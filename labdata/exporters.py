"""
Export utilities for labdata.

Serializes LabData to YAML or JSON files.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import json
import yaml
from pathlib import Path

from .models import LabData


def export_to_yaml(data: LabData, output_path: str):
    """Export LabData to a YAML file.

    Args:
        data: Assembled LabData instance
        output_path: Path to output YAML file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data.to_dict(), f, default_flow_style=False,
                  allow_unicode=True, sort_keys=False)


def export_to_json(data: LabData, output_path: str, indent: int = 2):
    """Export LabData to a JSON file.

    Args:
        data: Assembled LabData instance
        output_path: Path to output JSON file
        indent: Indentation level for pretty printing
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data.to_dict(), f, indent=indent, ensure_ascii=False)
