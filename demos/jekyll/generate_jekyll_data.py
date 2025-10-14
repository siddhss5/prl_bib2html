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
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from prl_bib2html import (
    LibraryConfig,
    list_publications,
    load_projects_config,
    list_publications_by_project,
    publications_to_dict,
    projects_to_dict,
    export_to_yaml
)

# Configuration
JEKYLL_SITE = Path.home() / "code" / "siddhss5.github.io"

# Load configuration from YAML file
config_path = Path(__file__).parent / "config.yaml"
lib_config = LibraryConfig.from_yaml(str(config_path))
CONFIG = lib_config.to_publications_config()


def generate_publications_yaml():
    """Generate publications.yml for Jekyll."""
    print("📚 Generating publications data...")
    
    # Get publications organized by year and category
    pubs = list_publications(CONFIG)
    
    # Convert to dict using library function
    yaml_data = publications_to_dict(pubs)
    
    # Write to Jekyll _data directory
    output_file = JEKYLL_SITE / "_data" / "publications.yml"
    export_to_yaml(yaml_data, str(output_file))
    
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
    
    # Sort projects (active first, then by newest pub, then alphabetical)
    def project_sort_key(item):
        project_name, project_info = item
        status = project_info.get('status', '').lower()
        status_priority = {'active': 0, 'archived': 1}.get(status, 2)
        
        newest_year = 0
        if project_name in project_pubs and project_pubs[project_name]:
            newest_year = max(pub.year for pub in project_pubs[project_name])
        
        return (status_priority, -newest_year, project_name)
    
    sorted_projects = dict(sorted(projects_config.items(), key=project_sort_key))
    
    # Convert to dict using library function
    yaml_data = projects_to_dict(sorted_projects, project_pubs)
    
    # Write to Jekyll _data directory
    output_file = JEKYLL_SITE / "_data" / "projects.yml"
    export_to_yaml(yaml_data, str(output_file))
    
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

