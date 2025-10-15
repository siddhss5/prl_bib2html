"""
Configuration schema for prl_bib2html.

This module provides dataclasses for loading configuration from YAML files,
enabling a clean separation between configuration and code.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class BibtexFile:
    """Configuration for a single BibTeX file."""
    name: str
    category: str


@dataclass
class BibtexConfig:
    """Configuration for BibTeX sources."""
    bib_dir: str
    files: List[BibtexFile]
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BibtexConfig':
        """Create from dictionary."""
        files = [BibtexFile(**f) for f in data.get('files', [])]
        return cls(
            bib_dir=data['bib_dir'],
            files=files
        )


@dataclass
class ProjectsConfig:
    """Configuration for projects."""
    config_file: str


@dataclass
class OutputConfig:
    """Configuration for output settings."""
    pdf_base_url: str


@dataclass
class LibraryConfig:
    """
    Main configuration class for prl_bib2html.
    
    This replaces PublicationsConfig with a more structured approach
    that can be loaded from YAML files.
    """
    bibtex: BibtexConfig
    output: OutputConfig
    projects: Optional[ProjectsConfig] = None
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'LibraryConfig':
        """
        Load configuration from YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            LibraryConfig instance
            
        Example YAML structure:
            bibtex:
              bib_dir: "data/bib"
              files:
                - name: "journal.bib"
                  category: "Journal Papers"
                - name: "conference.bib"
                  category: "Conference Papers"
            
            projects:
              config_file: "data/projects-config.yaml"
            
            output:
              pdf_base_url: "https://example.com/pdfs"
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        bibtex = BibtexConfig.from_dict(data['bibtex'])
        output = OutputConfig(**data['output'])
        projects = ProjectsConfig(**data['projects']) if 'projects' in data else None
        
        return cls(bibtex=bibtex, output=output, projects=projects)
    
    def to_publications_config(self):
        """
        Convert to legacy PublicationsConfig for backward compatibility.
        
        Returns:
            PublicationsConfig instance
        """
        from .publications import PublicationsConfig
        
        return PublicationsConfig(
            bibtex_base_url=None,  # No longer used
            bibtex_cache_dir=self.bibtex.bib_dir,
            pdf_base_dir=self.output.pdf_base_url,
            bib_files=[(f.name, f.category) for f in self.bibtex.files],
            projects_yaml_path=self.projects.config_file if self.projects else None
        )

