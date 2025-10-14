"""
PRL BibTeX to HTML converter module.

This module provides functionality to convert BibTeX files to HTML format
for displaying publications on a website.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

from .publications import (
    PublicationsConfig,
    Publication,
    list_publications,
    load_projects_config,
    list_publications_by_project
)
from .config_schema import (
    LibraryConfig,
    BibtexConfig,
    ProjectsConfig,
    OutputConfig,
    BibtexFile
)
from .exporters import (
    publication_to_dict,
    publications_to_dict,
    projects_to_dict,
    export_to_yaml,
    export_to_json
)

__all__ = [
    # Legacy API (backward compatible)
    "PublicationsConfig",
    "Publication",
    "list_publications",
    "load_projects_config",
    "list_publications_by_project",
    # New config-driven API
    "LibraryConfig",
    "BibtexConfig",
    "ProjectsConfig",
    "OutputConfig",
    "BibtexFile",
    # Export utilities
    "publication_to_dict",
    "publications_to_dict",
    "projects_to_dict",
    "export_to_yaml",
    "export_to_json"
]
__version__ = "1.0.0" 