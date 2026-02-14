"""
BibTeX parsing pipeline.

Parses BibTeX files into structured Publication dataclasses with
Markdown-formatted text (no HTML).

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import re
from pathlib import Path
from typing import List, Optional

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as parse_author

from ..latex import replace_latex_accents, latex_to_markdown, latex_to_text
from ..models import Author, Publication


def parse_bibtex_file(path: str) -> list:
    """Parse a BibTeX file and return raw entry dicts."""
    with open(path, 'r', encoding='utf-8') as f:
        parser = BibTexParser(common_strings=True)
        bib = bibtexparser.load(f, parser)
    return bib.entries


def parse_author_list(raw_author_field: str) -> List[Author]:
    """Parse a BibTeX author field into a list of Author dataclasses.

    Uses bibtexparser to split the field, then normalizes each name to
    "F. M. Last" abbreviated format. Returns Author objects with
    person_id=None (resolution happens later).
    """
    if not raw_author_field or not raw_author_field.strip():
        return []

    try:
        name_list = parse_author({'author': raw_author_field})['author']
    except Exception:
        return [Author(name=raw_author_field.strip())]

    authors = []
    for name in name_list:
        abbrev = _abbreviate_name(name)
        authors.append(Author(name=abbrev))
    return authors


def _abbreviate_name(name) -> str:
    """Abbreviate a parsed author name to 'F. M. Last' format."""
    if isinstance(name, str):
        name = replace_latex_accents(name)
        if ',' in name:
            last, first = [s.strip() for s in name.split(',', 1)]
            name = {'first': first, 'last': last}
        else:
            return name

    if not isinstance(name, dict):
        return str(name)

    last = name.get('last', '')
    last = replace_latex_accents(last)

    # Extract superscript affiliations from last name
    sup = ''
    match = re.search(r'(.*?)\$?\^\{(.+?)\}\$?$', last)
    if match:
        last = match.group(1)
        sup = f"<sup>{match.group(2)}</sup>"

    initials = ''
    if 'first' in name:
        first = replace_latex_accents(name['first'])
        cleaned = re.sub(r"\(.*?\)", "", first).strip()
        initials = ' '.join(
            part[0] + '.' for part in cleaned.split() if part
        )

    return f"{initials} {last}{sup}".strip()


def format_authors_string(authors: List[Author]) -> str:
    """Format a list of Authors into a display string.

    Uses 'and' for 2 authors, commas + 'and' for 3+.
    """
    names = [a.name for a in authors]
    if len(names) <= 2:
        return ' and '.join(names)
    return ', '.join(names[:-1]) + ', and ' + names[-1]


def format_venue(entry: dict) -> str:
    """Format venue string from a BibTeX entry dict. Uses Markdown (not HTML)."""
    typ = entry.get("ENTRYTYPE", "")
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
        if num:
            note += f" {num}"
        note += f", {inst}, {year}"
        return note
    elif typ == "misc":
        arxiv_id = entry.get("eprint")
        if arxiv_id:
            return f"*arXiv:{arxiv_id}*, {year}"
    elif typ == "article":
        journal = entry.get("journal", "").replace('{', '').replace('}', '')
        vol = entry.get("volume", "")
        num = entry.get("number", "")
        note = f"*{journal}*"
        if vol:
            note += f", {vol}"
            if num:
                note += f"({num})"
        if year:
            note += f", {year}"
        return note
    elif typ == "inproceedings":
        conf = entry.get("booktitle", "").replace('{', '').replace('}', '')
        conf = latex_to_text(conf)
        return f"*{conf}*, {year}" if conf else str(year)

    return str(year)


def extract_note(entry: dict) -> Optional[str]:
    """Extract and format the note field. Returns Markdown."""
    note = entry.get("note", "").strip().rstrip('. ')
    if not note:
        return None
    return latex_to_markdown(note)


def extract_video_url(entry: dict) -> Optional[str]:
    """Extract video URL if the entry's URL points to a video platform."""
    url = entry.get("url", "")
    if url and any(p in url for p in ["youtube.com", "youtu.be", "vimeo.com"]):
        return url
    return None


def construct_doi_url(entry: dict) -> Optional[str]:
    """Construct a DOI URL from the doi field."""
    doi = entry.get("doi")
    if doi:
        doi = doi.strip()
        if doi.startswith("http"):
            return doi
        return f"https://doi.org/{doi}"
    return None


def construct_arxiv_url(entry: dict) -> Optional[str]:
    """Construct an arXiv URL from the eprint field."""
    eprint = entry.get("eprint")
    if eprint:
        prefix = entry.get("archivePrefix", entry.get("archiveprefix", ""))
        if prefix.lower() == "arxiv" or not prefix:
            return f"https://arxiv.org/abs/{eprint}"
    return None


def parse_project_ids(entry: dict) -> List[str]:
    """Parse the project field from a BibTeX entry."""
    project_field = entry.get("project", "").strip()
    if not project_field:
        return []
    project_field = project_field.strip('{}')
    return [p.strip() for p in project_field.split(',') if p.strip()]


def resolve_pdf_url(bib_id: str, pdf_base_url: Optional[str]) -> Optional[str]:
    """Construct a PDF URL for a given bib entry."""
    if not pdf_base_url:
        return None
    pdf_path = f"{pdf_base_url}/{bib_id}.pdf"
    if pdf_base_url.startswith(('http://', 'https://')):
        return pdf_path
    return pdf_path if Path(pdf_path).exists() else None


def entry_to_publication(
    entry: dict,
    category: str,
    pdf_base_url: Optional[str] = None,
) -> Publication:
    """Convert a raw BibTeX entry dict to a Publication dataclass."""
    title = latex_to_markdown(entry.get("title", ""))
    authors = parse_author_list(entry.get("author", ""))

    # Extract URL (non-video)
    url = entry.get("url", "")
    video_url = extract_video_url(entry)
    if video_url:
        url = None  # Don't duplicate video URL in generic url field

    return Publication(
        bib_id=entry.get("ID", ""),
        title=title,
        authors=authors,
        year=int(entry.get("year", 0)),
        venue=format_venue(entry),
        category=category,
        entry_type=entry.get("ENTRYTYPE", ""),
        abstract=entry.get("abstract"),
        note=extract_note(entry),
        pdf_url=resolve_pdf_url(entry.get("ID", ""), pdf_base_url),
        doi_url=construct_doi_url(entry),
        arxiv_url=construct_arxiv_url(entry),
        url=url if url and not video_url else None,
        video_url=video_url,
        project_ids=parse_project_ids(entry),
    )


def parse_all_publications(
    bib_dir: str,
    bib_files: list,
    pdf_base_url: Optional[str] = None,
) -> List[Publication]:
    """Parse all configured BibTeX files and return a flat list of Publications.

    Args:
        bib_dir: Directory containing the BibTeX files
        bib_files: List of dicts with 'name' and 'category' keys
        pdf_base_url: Base URL/path for PDFs

    Returns:
        List of Publication objects, sorted by year descending
    """
    publications = []
    for bib_file in bib_files:
        name = bib_file['name'] if isinstance(bib_file, dict) else bib_file.name
        category = bib_file['category'] if isinstance(bib_file, dict) else bib_file.category
        path = f"{bib_dir}/{name}"
        entries = parse_bibtex_file(path)
        for entry in entries:
            pub = entry_to_publication(entry, category, pdf_base_url)
            publications.append(pub)

    publications.sort(key=lambda p: p.year, reverse=True)
    return publications
