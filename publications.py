import os
import re
import requests
from pathlib import Path
from collections import defaultdict

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as parse_author


PRL_PUBS = os.environ.get(
    "PRL_PUBS",
    "/cse/web/research/personalroboticslab/personalrobotics/publications/"
)

BIB_FILES = [
    ("siddpubs-journal.bib", "Journal Papers"),
    ("siddpubs-conf.bib", "Conference Papers"),
    ("siddpubs-misc.bib", "Other Papers"),
]


def latex_to_html(text):
    if not isinstance(text, str):
        return text

    math_blocks = []

    # Protect math expressions (e.g., $x^2$) so they're not corrupted
    def protect_math(m):
        math_blocks.append(m.group(1))
        return f"__MATH{len(math_blocks)-1}__"

    text = re.sub(r'\$(.*?)\$', protect_math, text)

    # Replace LaTeX formatting commands with HTML
    text = re.sub(r'\\textbf\{(.*?)\}', r'<b>\1</b>', text)
    text = re.sub(r'\\emph\{(.*?)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\href\{(.*?)\}\{(.*?)\}', r'<a href="\1">\2</a>', text)
    text = re.sub(r'\^\{(.*?)\}', r'<sup>\1</sup>', text)
    text = re.sub(r'_\{(.*?)\}', r'<sub>\1</sub>', text)

    # Strip any leftover braces
    text = text.replace('{', '').replace('}', '')

    # Restore protected math expressions
    def restore_math(m):
        math = math_blocks[int(m.group(1))]
        return f'<span class="math">\\({math}\\)</span>'

    text = re.sub(r'__MATH(\d+)__', restore_math, text)

    return text


def format_authors_structured(raw_author_field):
    try:
        name_list = parse_author({'author': raw_author_field})['author']
    except Exception:
        return raw_author_field

    def extract_superscript(last_name):
        match = re.search(r'(.*?)\$?\^\{(.+?)\}\$?$', last_name)
        if match:
            clean_last = match.group(1)
            sup = f"<sup>{match.group(2)}</sup>"
            return clean_last, sup
        return last_name, ''

    def abbrev(name):
        if isinstance(name, str):
            return name  # Fallback for unstructured names
        last, sup = extract_superscript(name.get('last', '') if isinstance(name, dict) else name)
        initials = ''
        if 'first' in name:
            cleaned_first = re.sub(r"\(.*?\)", "", name['first']).strip()
            initials = ' '.join([part[0] + '.' for part in cleaned_first.split() if part])
        return f"{initials} {last}{sup}".strip()

    def normalize_name(name):
        if isinstance(name, dict):
            return name
        if isinstance(name, str) and ',' in name:
            last, first = [s.strip() for s in name.split(',', 1)]
            return {'first': first, 'last': last}
        return {'first': name, 'last': ''}

    authors = [abbrev(normalize_name(n)) for n in name_list]

    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return ' and '.join(authors)
    return ', '.join(authors[:-1]) + ', and ' + authors[-1]


def fetch_bibtex(name):
    url = f"https://raw.githubusercontent.com/personalrobotics/pubs/master/{name}"
    cache_path = f"data/pubs/{name}"
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    if not os.path.exists(cache_path):
        response = requests.get(url)
        response.raise_for_status()
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

    with open(cache_path, 'r', encoding='utf-8') as f:
        parser = BibTexParser(common_strings=True)
        return bibtexparser.load(f, parser)


def pdf_path(entry_key):
    path = Path(PRL_PUBS) / f"{entry_key}.pdf"
    if path.exists():
        return f"/publications/{entry_key}.pdf"
    return None


def list_publications():
    all_entries = []
    for fname, pub_type in BIB_FILES:
        bib = fetch_bibtex(fname)
        for entry in bib.entries:
            entry["type"] = pub_type
            entry["year"] = int(entry.get("year", 0))
            entry["pdf"] = pdf_path(entry["ID"])
            # Custom type_note for thesis and techreport
            if entry["ENTRYTYPE"] == "phdthesis":
                entry["type_note"] = f"PhD thesis, {entry.get('school', '')}, {entry.get('year', '')}"
            elif entry["ENTRYTYPE"] == "mastersthesis":
                entry["type_note"] = f"Master’s thesis, {entry.get('school', '')}, {entry.get('year', '')}"
            elif entry["ENTRYTYPE"] == "techreport":
                report_type = entry.get("type", "Technical Report")
                report_number = entry.get("number", "")
                institution = entry.get("institution", "")
                year = entry.get("year", "")
                report_info = f"<b>{report_type}"
                if report_number:
                    report_info += f" {report_number}"
                report_info += f"</b>, {institution}, {year}"
                entry["type_note"] = report_info
            else:
                entry["type_note"] = ""
            for k in entry:
                if k == "author":
                    entry[k] = format_authors_structured(entry[k])
                entry[k] = latex_to_html(entry[k])
            all_entries.append(entry)

    all_entries.sort(key=lambda e: e["year"], reverse=True)

    grouped = defaultdict(lambda: defaultdict(list))
    for e in all_entries:
        grouped[e["year"]][e["type"]].append(e)

    return grouped


if __name__ == "__main__":
    pubs = list_publications()
    for year in sorted(pubs.keys(), reverse=True):
        print(f"\n==== {year} ====")
        for typ, entries in pubs[year].items():
            print(f"\n-- {typ} --")
            for e in entries:
                print(f"* {e.get('author', 'Unknown')} — {e.get('title', 'No Title')}")