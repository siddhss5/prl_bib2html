"""
PRL BibTeX to HTML converter module.

This module provides functionality to convert BibTeX files to HTML format
for displaying publications on a website.
"""

from .publications import PublicationsConfig, list_publications

__all__ = ["PublicationsConfig", "list_publications"]
__version__ = "1.0.0" 