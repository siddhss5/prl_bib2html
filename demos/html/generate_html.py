#!/usr/bin/env python3
"""
Standalone HTML generator for PRL publications.

This script demonstrates how to use the prl_bib2html library
to generate a complete HTML publications page without any web framework.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for development
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from prl_bib2html import PublicationsConfig, list_publications

def generate_html():
    """Generate a complete HTML publications page."""
    
    # PRL-specific configuration
    config = PublicationsConfig(
        bibtex_base_url="https://raw.githubusercontent.com/personalrobotics/pubs/refs/heads/siddhss5-href-flip-bug",
        bibtex_cache_dir="data/bib",
        pdf_base_dir="https://personalrobotics.cs.washington.edu/publications/",
        bib_files=[
            ("siddpubs-journal.bib", "Journal Papers"),
            ("siddpubs-conf.bib", "Conference Papers"),
            ("siddpubs-misc.bib", "Other Papers"),
        ]
    )
    
    # Get publications data
    publications = list_publications(config)
    
    # Generate HTML
    html_content = generate_publications_html(publications)
    
    # Write to file
    output_file = Path(__file__).parent / "publications.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {output_file}")
    total_pubs = sum(len(pubs) for year in publications.values() for pubs in year.values())
    print(f"📊 Found {total_pubs} publications")

def generate_publications_html(publications):
    """Generate HTML content."""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Robotics Lab - Publications</title>

    <!-- Bootstrap for layout -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">

    <!-- KaTeX for rendering LaTeX math -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {
            delimiters: [
                {left: '\\\\(', right: '\\\\)', display: false},
                {left: '\\\\[', right: '\\\\]', display: true}
            ]
        });">
    </script>

    <style>
        body {
            font-family: system-ui, sans-serif;
            padding-bottom: 4rem;
        }
        .math {
            font-family: inherit;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">PRL</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4" id="publications">
        <h1>Publications</h1>
"""
    
    for year in sorted(publications.keys(), reverse=True):
        html += f'        <h2 class="mt-5">{year}</h2>\n\n'
        
        for category, pubs in publications[year].items():
            html += f'        <h4 class="mt-4">{category}</h4>\n'
            html += f'        <ul class="list-unstyled">\n'
            
            for pub in pubs:
                html += f'            <li class="mb-3">\n'
                html += f'                <p class="mb-1">\n'
                
                if pub.pdf_url:
                    html += f'                    <a href="{pub.pdf_url}"><strong>{pub.title}</strong></a>\n'
                else:
                    html += f'                    <strong>{pub.title}</strong>\n'
                
                html += f'                </p>\n\n'
                html += f'                <p class="mb-1">{pub.authors}</p>\n\n'
                html += f'                <p class="mb-0">\n'
                
                if pub.venue:
                    html += f'                    {pub.venue}\n'
                
                if pub.note:
                    html += f'                    <br><b>{pub.note}</b>\n'
                
                html += f'                </p>\n'
                html += f'            </li>\n'
            
            html += f'        </ul>\n\n'
    
    html += """    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    generate_html() 