#!/usr/bin/env python3
"""
Standalone HTML generator demo for labdata.

Generates a complete HTML publications page from BibTeX sources.
This demonstrates how to consume labdata output in a custom renderer.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import sys
from pathlib import Path
from itertools import groupby

# Add the project root to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from labdata import LabDataConfig, assemble


def generate_html():
    """Generate a complete HTML publications page."""
    config_path = Path(__file__).parent / "config.yaml"
    config = LabDataConfig.from_yaml(str(config_path))
    data = assemble(config)

    # Build project lookup
    project_map = {p.id: p for p in data.projects}

    # Generate HTML
    pubs_html = generate_publications_html(data.publications, project_map)
    output_file = Path(__file__).parent / "publications.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pubs_html)

    print(f"Wrote {output_file}")
    print(f"  {len(data.publications)} publications")


def generate_publications_html(publications, project_map):
    """Generate HTML content from publications."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <style>
        body { font-family: system-ui, sans-serif; padding-bottom: 4rem; }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1>Publications</h1>
"""

    # Group by year
    sorted_pubs = sorted(publications, key=lambda p: (-p.year, p.category))
    for year, year_pubs in groupby(sorted_pubs, key=lambda p: p.year):
        html += f'        <h2 class="mt-5">{year}</h2>\n'

        year_list = list(year_pubs)
        for cat, cat_pubs in groupby(year_list, key=lambda p: p.category):
            html += f'        <h4 class="mt-4">{cat}</h4>\n'
            html += '        <ul class="list-unstyled">\n'

            for pub in cat_pubs:
                author_str = ", ".join(a.name for a in pub.authors)
                html += '            <li class="mb-3">\n'

                if pub.pdf_url:
                    html += f'                <a href="{pub.pdf_url}"><strong>{pub.title}</strong></a>\n'
                else:
                    html += f'                <strong>{pub.title}</strong>\n'

                html += f'                <br>{author_str}\n'
                html += f'                <br>{pub.venue}\n'

                if pub.note:
                    html += f'                <br><b>{pub.note}</b>\n'

                for pid in pub.project_ids:
                    if pid in project_map:
                        html += f'                <span class="badge bg-info">{project_map[pid].title}</span>\n'

                html += '            </li>\n'

            html += '        </ul>\n'

    html += """    </div>
</body>
</html>"""
    return html


if __name__ == "__main__":
    generate_html()
