"""
Export utilities for converting publications data to various formats.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import json
import yaml
from typing import Dict, List
from pathlib import Path


def publication_to_dict(pub) -> dict:
    """
    Convert a Publication dataclass to a dictionary.
    
    Args:
        pub: Publication instance
        
    Returns:
        Dictionary representation of the publication
    """
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


def publications_to_dict(publications: dict) -> dict:
    """
    Convert nested publications structure to plain dictionaries.
    
    Args:
        publications: Dict from list_publications() 
                     {year: {category: [Publication, ...]}}
        
    Returns:
        Dictionary with Publications converted to dicts
    """
    result = {}
    for year, categories in publications.items():
        result[year] = {}
        for category, pubs in categories.items():
            result[year][category] = [publication_to_dict(p) for p in pubs]
    return result


def projects_to_dict(projects_config: dict, project_pubs: dict) -> dict:
    """
    Convert projects data to dictionary format.
    
    Args:
        projects_config: Project metadata from YAML
        project_pubs: Publications grouped by project from list_publications_by_project()
        
    Returns:
        Dictionary with projects and their publications
    """
    result = {}
    for project_name, project_info in projects_config.items():
        result[project_name] = {
            'title': project_info.get('title', project_name),
            'description': project_info.get('description'),
            'website': project_info.get('website'),
            'status': project_info.get('status'),
            'publications': [
                publication_to_dict(pub)
                for pub in project_pubs.get(project_name, [])
            ]
        }
    return result


def export_to_yaml(data: dict, output_path: str):
    """
    Export data to YAML file.
    
    Args:
        data: Dictionary to export
        output_path: Path to output YAML file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def export_to_json(data: dict, output_path: str, indent: int = 2):
    """
    Export data to JSON file.
    
    Args:
        data: Dictionary to export
        output_path: Path to output JSON file
        indent: Indentation level for pretty printing
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

