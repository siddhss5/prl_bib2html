"""
Main pipeline orchestrator.

Assembles the complete LabData output from configuration:
config → parse BibTeX → load people/projects → resolve links → back-link.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

from typing import List, Optional

from .config import LabDataConfig
from .models import LabData, Publication
from .parsers.bibtex import parse_all_publications
from .loaders import load_people, load_projects
from .resolver import resolve_authors, resolve_projects, compute_backlinks


def assemble(config: LabDataConfig) -> LabData:
    """Main entry point: config → fully resolved LabData.

    1. Parse all BibTeX files into Publications
    2. Load people and projects from YAML
    3. Resolve author names → person IDs
    4. Validate project IDs
    5. Compute back-links (people→pubs, projects→pubs, projects→people)

    Returns:
        LabData with all cross-references resolved
    """
    # Parse publications
    bib_files = [{'name': bf.name, 'category': bf.category} for bf in config.bib_files]
    publications = parse_all_publications(
        bib_dir=config.bib_dir,
        bib_files=bib_files,
        pdf_base_url=config.pdf_base_url,
    )

    # Load people and projects
    people = load_people(config.people_file) if config.people_file else []
    projects = load_projects(config.projects_file) if config.projects_file else []

    # Resolve
    resolve_authors(publications, people)
    resolve_projects(publications, projects)

    # Assemble
    data = LabData(
        publications=publications,
        people=people,
        projects=projects,
    )

    # Back-link
    compute_backlinks(data)

    return data
