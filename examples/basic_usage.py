#!/usr/bin/env python3
"""
Basic usage example for prl_bib2html.

This demonstrates the simple Python API for generating publication data.
"""

from pathlib import Path
from prl_bib2html import (
    LibraryConfig,
    list_publications,
    load_projects_config,
    list_publications_by_project,
    publications_to_dict,
    projects_to_dict,
    export_to_yaml,
    export_to_json
)

# Example 1: Load from YAML config file
print("Example 1: Using YAML configuration")
print("=" * 50)

config = LibraryConfig.from_yaml("config.yaml")
pubs = list_publications(config.to_publications_config())

# Convert to dict for export
pubs_dict = publications_to_dict(pubs)

# Export to YAML
export_to_yaml(pubs_dict, "output/publications.yml")
print(f"✅ Exported to output/publications.yml")

# Export to JSON
export_to_json(pubs_dict, "output/publications.json")
print(f"✅ Exported to output/publications.json")


# Example 2: Working with projects
print("\n\nExample 2: Working with projects")
print("=" * 50)

legacy_config = config.to_publications_config()
if legacy_config.projects_yaml_path:
    projects_config = load_projects_config(legacy_config.projects_yaml_path)
    project_pubs = list_publications_by_project(legacy_config, projects_config)
    
    # Convert to dict
    projects_dict = projects_to_dict(projects_config, project_pubs)
    
    # Export
    export_to_yaml(projects_dict, "output/projects.yml")
    print(f"✅ Exported to output/projects.yml")


# Example 3: Working with raw data (no export)
print("\n\nExample 3: Working with raw Python data")
print("=" * 50)

pubs = list_publications(legacy_config)

# Iterate through publications
for year, categories in sorted(pubs.items(), reverse=True):
    print(f"\nYear {year}:")
    for category, publications in categories.items():
        print(f"  {category}: {len(publications)} papers")
        for pub in publications[:2]:  # Show first 2
            print(f"    - {pub.title[:60]}...")

