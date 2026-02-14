# labdata

Renderer-agnostic academic lab data assembler.

## Overview

`labdata` transforms BibTeX files and simple YAML configuration into structured data (YAML/JSON) for academic lab websites. It resolves cross-references between publications, people, and projects into a single connected dataset that any downstream renderer can consume.

**Input:** BibTeX files + YAML for people and projects + one config file

**Output:** Structured YAML/JSON with resolved cross-references

Works with Jekyll, Hugo, Flask, React, or any other framework.

## Features

- **BibTeX Processing**: Parse BibTeX files with rich academic metadata
- **LaTeX to Markdown**: Convert LaTeX accents, formatting, and math to Markdown
- **Author Resolution**: Match publication authors to lab members via aliases + fuzzy matching
- **People & Projects**: Track lab members (current + alumni) and research projects
- **Cross-References**: Automatic back-linking between publications, people, and projects
- **Multiple Outputs**: Export to YAML or JSON
- **Validation**: CLI flags to check data quality and find unresolved authors

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
git clone https://github.com/personalrobotics/labdata.git
cd labdata
uv pip install -e .
```

## Quick Start

### 1. Create a config file (`lab.yaml`)

```yaml
bib_dir: "data/bib"
bib_files:
  - name: "journal.bib"
    category: "Journal Papers"
  - name: "conference.bib"
    category: "Conference Papers"

pdf_base_url: "https://your-site.com/pdfs"
people_file: "data/people.yaml"
projects_file: "data/projects.yaml"
```

### 2. Generate data

```bash
labdata --config lab.yaml --output lab.yml
```

### 3. Validate

```bash
# Check data quality
labdata --config lab.yaml --validate

# See unresolved author names
labdata --config lab.yaml --unresolved
```

### Python API

```python
from labdata import LabDataConfig, assemble, export_to_yaml

config = LabDataConfig.from_yaml("lab.yaml")
data = assemble(config)
export_to_yaml(data, "lab.yml")

# Access the data directly
for pub in data.publications:
    print(pub.title, [a.name for a in pub.authors])
```

## Data Model

### Publications

Each BibTeX entry becomes a `Publication` with structured, renderer-agnostic fields:

```yaml
publications:
  - bib_id: "smith2024robot"
    title: "Robot-Assisted Feeding"     # Markdown, not HTML
    authors:
      - name: "J. Smith"
        person_id: "jsmith"            # resolved to people.yaml
      - name: "E. External"
        person_id: null                # external collaborator
    year: 2024
    venue: "*IEEE T-RO*, 2024"         # Markdown
    category: "Journal Papers"
    doi_url: "https://doi.org/..."
    project_ids: ["robotfeeding"]
```

### People (`data/people.yaml`)

```yaml
- id: "jsmith"
  name: "John Smith"
  aliases: ["J. Smith", "John A. Smith"]
  role: "pi"
  status: "current"
  website: "https://jsmith.example.com"

- id: "jdoe"
  name: "Jane Doe"
  aliases: ["J. Doe"]
  role: "phd_student"
  status: "alumni"
  end_year: 2023
  degree: "PhD"
  current_position: "Research Scientist at Google"
```

### Projects (`data/projects.yaml`)

```yaml
- id: "robotfeeding"
  title: "Robot-Assisted Feeding"
  description: "Autonomous feeding systems"
  website: "https://robotfeeding.io"
  status: "active"
```

### BibTeX Project Tags

Tag publications with projects using the `project` field in BibTeX:

```bibtex
@inproceedings{smith2024,
  title = {My Paper},
  author = {Smith, J.},
  year = {2024},
  project = {robotics, planning}
}
```

## Demos

- `demos/jekyll/` - Jekyll/GitHub Pages data generator
- `demos/html/` - Standalone HTML page generator
- `demos/flask/` - Flask web application

## Dependencies

- `bibtexparser` - BibTeX parsing
- `pyyaml` - YAML I/O
- `Flask` (optional) - For Flask demo

## License

MIT License - see [LICENSE](LICENSE) for details.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
