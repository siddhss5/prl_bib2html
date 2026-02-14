#!/usr/bin/env python3
"""
Basic usage example for labdata.

This demonstrates the Python API for assembling academic lab data.
"""

from pathlib import Path
from labdata import LabDataConfig, assemble, export_to_yaml, export_to_json

# Example 1: Assemble data from config file
print("Example 1: Assemble from YAML config")
print("=" * 50)

config = LabDataConfig.from_yaml("config.yaml")
data = assemble(config)

print(f"Publications: {len(data.publications)}")
print(f"People: {len(data.people)}")
print(f"Projects: {len(data.projects)}")

# Export to YAML
export_to_yaml(data, "output/lab.yml")
print("Exported to output/lab.yml")

# Export to JSON
export_to_json(data, "output/lab.json")
print("Exported to output/lab.json")


# Example 2: Inspect the data
print("\n\nExample 2: Working with the data")
print("=" * 50)

for pub in data.publications[:3]:
    author_names = ", ".join(a.name for a in pub.authors)
    print(f"\n{pub.title}")
    print(f"  {author_names}")
    print(f"  {pub.venue}")
    if pub.project_ids:
        print(f"  Projects: {', '.join(pub.project_ids)}")

for person in data.people:
    print(f"\n{person.name} ({person.role}, {person.status})")
    print(f"  {person.publication_count} publications")
