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
    list_publications,
    load_projects_config,
    list_publications_by_project
)

__all__ = [
    "PublicationsConfig",
    "list_publications",
    "load_projects_config",
    "list_publications_by_project"
]
__version__ = "1.0.0" 