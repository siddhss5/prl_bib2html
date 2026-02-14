"""
labdata - Renderer-agnostic academic lab data assembler.

Transforms BibTeX files and YAML configuration into structured data
(YAML/JSON) for academic lab websites. Framework-agnostic: works with
Jekyll, Hugo, Flask, or any other consumer.

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
__version__ = "2.0.0-dev"
