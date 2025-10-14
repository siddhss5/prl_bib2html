"""
BibTeX to HTML conversion utilities.

This module provides functions for parsing BibTeX files and converting them
to HTML format for academic publications websites.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import os
import re
import requests
import yaml
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, List, Dict

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as parse_author

LATEX_ACCENTS = {
    "\\'e": "é", "\\'E": "É",
    "\\'a": "á", "\\'A": "Á",
    "\\'i": "í", "\\'I": "Í",
    "\\'o": "ó", "\\'O": "Ó",
    "\\'u": "ú", "\\'U": "Ú",
    '\\"u': "ü", '\\"U': "Ü",
    '\\"a': "ä", '\\"A': "Ä",
    '\\"o': "ö", '\\"O': "Ö"
}

def replace_latex_accents(text: str) -> str:
    for latex, uni in LATEX_ACCENTS.items():
        text = text.replace(latex, uni)
    return text

@dataclass
class PublicationsConfig:
    """
    Configuration for publications processing.
    
    Attributes:
        bibtex_base_url: Base URL for fetching BibTeX files
        bibtex_cache_dir: Local directory for caching BibTeX files
        pdf_base_dir: Base directory/URL for PDF files. Can be either:
                     - Local path (e.g., "data/pdf") - will check if files exist
                     - URL (e.g., "https://example.com/pdfs") - will construct URLs directly
        bib_files: List of (filename, display_name) tuples for BibTeX files
        projects_yaml_path: Optional path to projects YAML file
    """
    bibtex_base_url: str
    bibtex_cache_dir: str
    pdf_base_dir: str
    bib_files: List[tuple]
    projects_yaml_path: Optional[str] = None

@dataclass
class Publication:
    entry_type: str
    year: int
    title: str
    authors: str
    venue: str
    note: str
    pdf_url: Optional[str]
    projects: List[str]
    
    def to_dict(self) -> dict:
        """Convert Publication to dictionary for serialization."""
        return {
            'title': self.title,
            'authors': self.authors,
            'venue': self.venue,
            'year': self.year,
            'pdf_url': self.pdf_url,
            'note': self.note if self.note else None,
            'projects': self.projects if self.projects else [],
            'entry_type': self.entry_type
        }

def latex_to_html(text: str) -> str:
    if not isinstance(text, str):
        return text
    math_blocks = []
    def protect_math(m):
        math_blocks.append(m.group(1))
        return f"__MATH{len(math_blocks)-1}__"
    text = re.sub(r'\$(.*?)\$', protect_math, text)
    text = re.sub(r'\\textbf\{(.*?)\}', r'<b>\1</b>', text)
    text = re.sub(r'\\textbf\s*', '', text)
    text = re.sub(r'\\emph\{(.*?)\}', r'<em>\1</em>', text)
    # Handle \href{url}{text} and \href{url} cases
    text = re.sub(r'\\href\{(.*?)\}\{(.*?)\}', r'<a href="\1">\2</a>', text)
    text = re.sub(r'\\href\{(.*?)\}', r'<a href="\1">\1</a>', text)
    text = re.sub(r'\^\{(.*?)\}', r'<sup>\1</sup>', text)
    text = re.sub(r'_\{(.*?)\}', r'<sub>\1</sub>', text)
    # Remove remaining curly braces after LaTeX processing
    text = text.replace('{', '').replace('}', '')
    def restore_math(m):
        math = math_blocks[int(m.group(1))]
        return f'<span class="math">\\({math}\\)</span>'
    return re.sub(r'__MATH(\d+)__', restore_math, text)

def format_authors(raw_author_field: str) -> str:
    try:
        name_list = parse_author({'author': raw_author_field})['author']
    except Exception:
        return raw_author_field
    def extract_superscript(last_name):
        match = re.search(r'(.*?)\$?\^\{(.+?)\}\$?$', last_name)
        if match:
            return match.group(1), f"<sup>{match.group(2)}</sup>"
        return last_name, ''
    def abbrev(name):
        if isinstance(name, str): return name
        last, sup = extract_superscript(name.get('last', ''))
        initials = ''
        if 'first' in name:
            cleaned_first = re.sub(r"\(.*?\)", "", name['first']).strip()
            initials = ' '.join([part[0] + '.' for part in cleaned_first.split() if part])
        return f"{initials} {last}{sup}".strip()
    def normalize_name(name):
        if isinstance(name, dict):
            return name
        if isinstance(name, str):
            name = replace_latex_accents(name)
            if ',' in name:
                last, first = [s.strip() for s in name.split(',', 1)]
                return {'first': first, 'last': last}
            return {'first': name, 'last': ''}
        return {'first': '', 'last': ''}
    authors = [abbrev(normalize_name(n)) for n in name_list]
    if len(authors) <= 2:
        return ' and '.join(authors)
    return ', '.join(authors[:-1]) + ', and ' + authors[-1]

def fetch_bibtex(name: str, config: PublicationsConfig):
    bib_url = f"{config.bibtex_base_url}/{name}"
    bib_path = f"{config.bibtex_cache_dir}/{name}"
    os.makedirs(os.path.dirname(bib_path), exist_ok=True)
    if not os.path.exists(bib_path):
        response = requests.get(bib_url)
        response.raise_for_status()
        with open(bib_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
    with open(bib_path, 'r', encoding='utf-8') as f:
        parser = BibTexParser(common_strings=True)
        return bibtexparser.load(f, parser)

def format_pdf_url(name: str, config: PublicationsConfig) -> Optional[str]:
    pdf_path = f"{config.pdf_base_dir}/{name}.pdf"
    
    # Check if pdf_base_dir is a URL (starts with http:// or https://)
    if config.pdf_base_dir.startswith(('http://', 'https://')):
        # For URLs, return the constructed URL directly
        # Note: We don't check if the URL exists as that would require HTTP requests
        return pdf_path
    else:
        # For local paths, check if file exists
        return pdf_path if Path(pdf_path).exists() else None

def format_venue(entry) -> str:
    typ = entry.get("ENTRYTYPE")
    year = entry.get("year", "")
    if typ == "phdthesis":
        return f"PhD thesis, {entry.get('school', '')}, {year}"
    elif typ == "mastersthesis":
        return f"Masters thesis, {entry.get('school', '')}, {year}"
    elif typ == "techreport":
        kind = entry.get("type", "Technical Report")
        num = entry.get("number", "")
        inst = entry.get("institution", "")
        note = kind
        if num: note += f" {num}"
        note += f", {inst}, {year}"
        return note
    elif typ == "misc":
        arxiv_id = entry.get("eprint")
        if arxiv_id:
            return f'In <em>arXiv:{arxiv_id}</em>, {year}'
    elif typ == "article":
        journal = entry.get("journal", "").replace('{', '').replace('}', '')
        vol = entry.get("volume", "")
        num = entry.get("number", "")
        note = f"<em>{journal}</em>"
        if vol:
            note += f", {vol}"
            if num: note += f"({num})"
        if year: note += f", {year}"
        return note
    elif typ == "inproceedings":
        conf = latex_to_html(entry.get("booktitle", "").replace('{', '').replace('}', ''))
        return f"<em>{conf}</em>, {year}" if conf else str(year)
    return str(year)

def format_title(title: str) -> str:
    title = replace_latex_accents(title)
    title = latex_to_html(title)
    return title

def format_note(entry) -> str:
    note = latex_to_html(entry.get("note", "").strip().rstrip('. '))
    url = entry.get("url", "")
    if url: 
        if any(platform in url for platform in ["youtube.com", "youtu.be", "vimeo.com"]):
            return f'<a href="{url}">Video</a>{". " + note}'   
        else:
            return f'<a href="{url}">URL</a>{". " + note}'
    return note

def parse_projects(entry) -> List[str]:
    """Parse project field from BibTeX entry, supporting multiple projects."""
    project_field = entry.get("project", "").strip()
    if not project_field:
        return []
    
    # Remove surrounding braces and split by comma
    project_field = project_field.strip('{}')
    projects = [p.strip() for p in project_field.split(',') if p.strip()]
    return projects

def format_entry(entry, pub_type: str, config: PublicationsConfig) -> Publication:
    return Publication(
        entry_type=pub_type,
        year=int(entry.get("year", 0)),
        title=format_title(entry.get("title", "")),
        authors=format_authors(entry.get("author", "")),
        venue=format_venue(entry),
        note=format_note(entry),
        pdf_url=format_pdf_url(entry["ID"], config),
        projects=parse_projects(entry)
    )

def list_publications(config: PublicationsConfig) -> dict:
    all_entries = []
    for fname, pub_type in config.bib_files:
        bib = fetch_bibtex(fname, config)
        for entry in bib.entries:
            all_entries.append(format_entry(entry, pub_type, config))
    all_entries.sort(key=lambda e: e.year, reverse=True)
    grouped = defaultdict(lambda: defaultdict(list))
    for e in all_entries:
        grouped[e.year][e.entry_type].append(e)
    return grouped

def load_projects_config(yaml_path: str) -> Dict:
    """Load projects configuration from YAML file."""
    if not os.path.exists(yaml_path):
        return {}
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        projects = yaml.safe_load(f) or {}
    
    return projects

def list_publications_by_project(config: PublicationsConfig, projects_config: Dict) -> Dict[str, List[Publication]]:
    """
    Group publications by project.
    
    Args:
        config: Publications configuration
        projects_config: Dictionary of project metadata from YAML
    
    Returns:
        Dictionary mapping project names to lists of publications
    """
    all_entries = []
    for fname, pub_type in config.bib_files:
        bib = fetch_bibtex(fname, config)
        for entry in bib.entries:
            all_entries.append(format_entry(entry, pub_type, config))
    
    # Group by project, filtering to only valid projects
    project_pubs = defaultdict(list)
    for pub in all_entries:
        for project_name in pub.projects:
            if project_name in projects_config:
                project_pubs[project_name].append(pub)
    
    # Sort publications within each project by year (newest first)
    for project_name in project_pubs:
        project_pubs[project_name].sort(key=lambda e: e.year, reverse=True)
    
    return dict(project_pubs)
