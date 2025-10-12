#!/usr/bin/env python3
"""
Jekyll Data Generator for goodrobot.ai

This script generates Jekyll-compatible YAML data files from BibTeX sources
for use with Minimal Mistakes theme on GitHub Pages.

Usage:
    python generate_jekyll_data.py

Outputs:
    - <jekyll_site>/_data/publications.yml
    - <jekyll_site>/_data/projects.yml

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import os
import sys
import yaml
from pathlib import Path

# Add parent directory to path to import prl_bib2html
sys.path.insert(0, str(Path(__file__).parent.parent))

from prl_bib2html import (
    PublicationsConfig,
    list_publications,
    load_projects_config,
    list_publications_by_project
)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
JEKYLL_SITE = Path.home() / "code" / "siddhss5.github.io"

# PRL configuration
CONFIG = PublicationsConfig(
    bibtex_base_url="https://raw.githubusercontent.com/personalrobotics/pubs/refs/heads/siddhss5-href-flip-bug",
    bibtex_cache_dir=str(PROJECT_ROOT / "data" / "bib"),
    pdf_base_dir="https://personalrobotics.cs.washington.edu/publications/",
    bib_files=[
        ("siddpubs-journal.bib", "Journal Papers"),
        ("siddpubs-conf.bib", "Conference Papers"),
        ("siddpubs-misc.bib", "Other Papers"),
    ],
    projects_yaml_path=str(PROJECT_ROOT / "data" / "projects.yaml")
)


def publication_to_dict(pub):
    """Convert Publication dataclass to dictionary for YAML export."""
    return {
        'title': pub.title,
        'authors': pub.authors,
        'venue': pub.venue,
        'year': pub.year,
        'pdf_url': pub.pdf_url,
        'note': pub.note if pub.note else None,
        'projects': pub.projects if pub.projects else [],
        'entry_type': pub.entry_type
    }


def generate_publications_yaml():
    """Generate publications.yml for Jekyll."""
    print("📚 Generating publications data...")
    
    # Get publications organized by year and category
    pubs = list_publications(CONFIG)
    
    # Convert to YAML-friendly format
    yaml_data = {}
    for year, categories in sorted(pubs.items(), reverse=True):
        yaml_data[year] = {}
        for category, publications in categories.items():
            yaml_data[year][category] = [
                publication_to_dict(pub) for pub in publications
            ]
    
    # Write to Jekyll _data directory
    output_file = JEKYLL_SITE / "_data" / "publications.yml"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    total_pubs = sum(len(pubs) for year in yaml_data.values() for pubs in year.values())
    print(f"✅ Generated: {output_file}")
    print(f"   Found {total_pubs} publications across {len(yaml_data)} years")
    
    return yaml_data


def generate_projects_yaml():
    """Generate projects.yml for Jekyll."""
    print("\n📁 Generating projects data...")
    
    # Load projects configuration
    projects_config = load_projects_config(CONFIG.projects_yaml_path) if CONFIG.projects_yaml_path else {}
    
    if not projects_config:
        print("⚠️  No projects configured in projects.yaml")
        return {}
    
    # Get publications grouped by project
    project_pubs = list_publications_by_project(CONFIG, projects_config)
    
    # Build YAML data with projects sorted (active first, then by newest pub, then alphabetical)
    def project_sort_key(item):
        project_name, project_info = item
        status = project_info.get('status', '').lower()
        status_priority = {'active': 0, 'archived': 1}.get(status, 2)
        
        newest_year = 0
        if project_name in project_pubs and project_pubs[project_name]:
            newest_year = max(pub.year for pub in project_pubs[project_name])
        
        return (status_priority, -newest_year, project_name)
    
    yaml_data = {}
    for project_name, project_info in sorted(projects_config.items(), key=project_sort_key):
        yaml_data[project_name] = {
            'title': project_info.get('title', project_name),
            'description': project_info.get('description'),
            'website': project_info.get('website'),
            'status': project_info.get('status'),
            'publications': [
                publication_to_dict(pub)
                for pub in project_pubs.get(project_name, [])
            ]
        }
    
    # Write to Jekyll _data directory
    output_file = JEKYLL_SITE / "_data" / "projects.yml"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    total_project_pubs = sum(len(p['publications']) for p in yaml_data.values())
    print(f"✅ Generated: {output_file}")
    print(f"   Found {len(yaml_data)} projects with {total_project_pubs} publications")
    
    return yaml_data


def main():
    """Generate all Jekyll data files."""
    print("=" * 60)
    print("Jekyll Data Generator for goodrobot.ai")
    print("=" * 60)
    
    # Check if Jekyll site exists
    if not JEKYLL_SITE.exists():
        print(f"❌ Jekyll site not found at: {JEKYLL_SITE}")
        print(f"   Please update JEKYLL_SITE path in this script")
        sys.exit(1)
    
    print(f"\n📂 Jekyll site: {JEKYLL_SITE}")
    print(f"📂 Data source: {CONFIG.bibtex_cache_dir}")
    
    # Generate data files
    generate_publications_yaml()
    generate_projects_yaml()
    
    print("\n" + "=" * 60)
    print("✨ Done! Next steps:")
    print("=" * 60)
    print("1. Review generated files:")
    print(f"   {JEKYLL_SITE}/_data/publications.yml")
    print(f"   {JEKYLL_SITE}/_data/projects.yml")
    print("\n2. Update Jekyll pages:")
    print(f"   {JEKYLL_SITE}/_pages/publications.md")
    print(f"   {JEKYLL_SITE}/_pages/projects.md (create if needed)")
    print("\n3. Test locally:")
    print(f"   cd {JEKYLL_SITE}")
    print("   bundle exec jekyll serve")
    print("\n4. Commit and push to deploy")
    print("=" * 60)


if __name__ == "__main__":
    main()

