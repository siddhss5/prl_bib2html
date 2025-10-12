#!/usr/bin/env python3
"""
Standalone HTML generator for PRL publications.

This script demonstrates how to use the prl_bib2html library
to generate a complete HTML publications page without any web framework.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for development
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from prl_bib2html import (
    PublicationsConfig,
    list_publications,
    load_projects_config,
    list_publications_by_project
)

def generate_html():
    """Generate a complete HTML publications page."""
    
    # Get the root directory of the project (two levels up from this file)
    root_dir = Path(__file__).parent.parent.parent
    
    # PRL-specific configuration
    config = PublicationsConfig(
        bibtex_base_url="https://raw.githubusercontent.com/personalrobotics/pubs/refs/heads/siddhss5-href-flip-bug",
        bibtex_cache_dir=str(root_dir / "data" / "bib"),
        pdf_base_dir="https://personalrobotics.cs.washington.edu/publications/",
        bib_files=[
            ("siddpubs-journal.bib", "Journal Papers"),
            ("siddpubs-conf.bib", "Conference Papers"),
            ("siddpubs-misc.bib", "Other Papers"),
        ],
        projects_yaml_path=str(root_dir / "data" / "projects.yaml")
    )
    
    # Get publications data
    publications = list_publications(config)
    
    # Get projects data
    projects_config = load_projects_config(config.projects_yaml_path) if config.projects_yaml_path else {}
    project_pubs = list_publications_by_project(config, projects_config)
    
    # Generate HTML files
    pubs_html = generate_publications_html(publications, projects_config)
    projects_html = generate_projects_html(projects_config, project_pubs)
    
    # Write publications file
    output_file = Path(__file__).parent / "publications.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pubs_html)
    
    print(f"✅ Generated: {output_file}")
    total_pubs = sum(len(pubs) for year in publications.values() for pubs in year.values())
    print(f"📊 Found {total_pubs} publications")
    
    # Write projects file
    projects_output = Path(__file__).parent / "projects.html"
    with open(projects_output, 'w', encoding='utf-8') as f:
        f.write(projects_html)
    
    print(f"✅ Generated: {projects_output}")
    print(f"📊 Found {len(projects_config)} projects")

def generate_publications_html(publications, projects_config):
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
                    <li class="nav-item"><a class="nav-link" href="publications.html">Publications</a></li>
                    <li class="nav-item"><a class="nav-link" href="projects.html">Projects</a></li>
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
                
                if pub.projects:
                    html += f'                    <br>\n'
                    for project in pub.projects:
                        if project in projects_config:
                            html += f'                    <a href="projects.html#{project}" class="badge bg-info text-decoration-none">{project}</a> \n'
                
                html += f'                </p>\n'
                html += f'            </li>\n'
            
            html += f'        </ul>\n\n'
    
    html += """    </div>
</body>
</html>"""
    
    return html

def generate_projects_html(projects_config, project_pubs):
    """Generate HTML content for projects page."""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Robotics Lab - Projects</title>

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
                    <li class="nav-item"><a class="nav-link" href="publications.html">Publications</a></li>
                    <li class="nav-item"><a class="nav-link" href="projects.html">Projects</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Projects</h1>
"""
    
    if projects_config:
        # Sort projects: active first, then by newest publication, then alphabetically
        def project_sort_key(item):
            project_name, project_info = item
            # Status priority: active=0, archived=1, other=2
            status = project_info.get('status', '').lower()
            status_priority = {'active': 0, 'archived': 1}.get(status, 2)
            
            # Get newest publication year (or 0 if no publications)
            newest_year = 0
            if project_name in project_pubs and project_pubs[project_name]:
                newest_year = max(pub.year for pub in project_pubs[project_name])
            
            # Return tuple: (status_priority, -newest_year for descending, project_name)
            return (status_priority, -newest_year, project_name)
        
        sorted_projects = sorted(projects_config.items(), key=project_sort_key)
        
        for project_name, project_info in sorted_projects:
            # Use title if available, otherwise use project_name
            title = project_info.get('title', project_name)
            html += f'        <div class="mt-4 border-bottom pb-3" id="{project_name}">\n'
            html += f'            <h3>\n'
            html += f'                {title}\n'
            html += f'                <span class="badge bg-info text-decoration-none ms-2">{project_name}</span>\n'
            
            if project_info.get('status'):
                status = project_info['status']
                badge_color = 'success' if status == 'active' else 'secondary'
                html += f'                <span class="badge bg-{badge_color} ms-1">{status.capitalize()}</span>\n'
            
            if project_info.get('website'):
                html += f'                <a href="{project_info["website"]}" target="_blank" class="badge bg-primary text-decoration-none ms-1">Website</a>\n'
            
            html += f'            </h3>\n\n'
            
            if project_info.get('description'):
                html += f'            <p class="mb-2">{project_info["description"]}</p>\n\n'
            
            if project_name in project_pubs and project_pubs[project_name]:
                html += f'            <ul class="list-unstyled">\n'
                
                for pub in project_pubs[project_name]:
                    html += f'                <li class="mb-2">\n'
                    
                    if pub.pdf_url:
                        html += f'                    <a href="{pub.pdf_url}">{pub.title}</a>\n'
                    else:
                        html += f'                    {pub.title}\n'
                    
                    html += f'                    <br>\n'
                    html += f'                    <small class="text-muted">{pub.authors} — {pub.venue}</small>\n'
                    
                    if pub.note:
                        html += f'                    <br><small><b>{pub.note}</b></small>\n'
                    
                    html += f'                </li>\n'
                
                html += f'            </ul>\n'
            
            html += f'        </div>\n\n'
    else:
        html += '        <p class="lead">No projects configured.</p>\n'
    
    html += """    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    generate_html() 