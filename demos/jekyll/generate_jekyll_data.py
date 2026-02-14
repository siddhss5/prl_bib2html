#!/usr/bin/env python3
"""
Jekyll Data Generator Demo

Generates Jekyll-compatible YAML data files from BibTeX sources
for use with static site generators like Jekyll with Minimal Mistakes theme.

Usage:
    python generate_jekyll_data.py

Outputs:
    - lab.yml (publications, people, projects - all in one file)

This file can then be copied to your Jekyll site's _data/ directory.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import sys
from pathlib import Path

# Add parent directory to path to import labdata
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from labdata import LabDataConfig, assemble, export_to_yaml

# Load configuration
config_path = Path(__file__).parent / "config.yaml"
config = LabDataConfig.from_yaml(str(config_path))

# Assemble all data
data = assemble(config)

# Export
output_file = Path(__file__).parent / "lab.yml"
export_to_yaml(data, str(output_file))

print(f"Wrote {output_file}")
print(f"  {len(data.publications)} publications, "
      f"{len(data.people)} people, "
      f"{len(data.projects)} projects")
print()
print("Next steps:")
print("  cp lab.yml <your-jekyll-site>/_data/")
print("  cd <your-jekyll-site> && bundle exec jekyll serve")
