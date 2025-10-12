# Projects Feature Documentation

## Overview

The project support feature allows you to organize publications by research projects using BibTeX tags and a YAML configuration file. This enables you to create dedicated project pages showing all related papers and their metadata.

## Key Features

- **Project Organization**: Group publications by project using BibTeX `project` field
- **Multiple Projects Per Paper**: Support for papers that belong to multiple projects
- **Project Metadata**: Store project descriptions, websites, and status in YAML
- **Filtering**: Only display projects that are defined in the YAML configuration
- **Project Badges**: Display project tags on the publications page with links to project details
- **Bidirectional Navigation**: Navigate from publications to projects and vice versa

## Setup

### 1. BibTeX Files

Add a `project` field to your BibTeX entries:

```bibtex
@inproceedings{smith2024robot,
  title = {Advanced Robot Manipulation},
  author = {Smith, J. and Doe, A.},
  booktitle = {IEEE ICRA},
  year = {2024},
  project = {ada}
}

% For multiple projects:
@article{jones2024learning,
  title = {Learning to Grasp},
  author = {Jones, B.},
  journal = {Robotics Journal},
  year = {2024},
  project = {ada, herbpy}
}
```

### 2. Projects YAML File

Create a `data/projects.yaml` file with your project metadata:

```yaml
ada:
  title: "ADA - Assistive Dexterous Arm"
  description: "A robot for helping people with mobility impairments"
  website: "https://personalrobotics.cs.washington.edu/projects/ada"
  status: "active"

herbpy:
  title: "HERB Python Interface"
  description: "Software framework for the HERB robot"
  website: "https://github.com/personalrobotics/herbpy"
  status: "archived"

dart:
  title: "DART - Dynamic Animation and Robotics Toolkit"
  description: "Physics simulation library for robotics"
  website: "https://dartsim.github.io"
  status: "active"
```

### 3. Configuration

Update your `PublicationsConfig` to include the projects YAML path:

```python
from prl_bib2html import PublicationsConfig

config = PublicationsConfig(
    bibtex_base_url="https://example.com/pubs",
    bibtex_cache_dir="data/bib",
    pdf_base_dir="https://example.com/pdfs",
    bib_files=[
        ("journal.bib", "Journal Papers"),
        ("conference.bib", "Conference Papers"),
    ],
    projects_yaml_path="data/projects.yaml"  # Add this line
)
```

## Usage

### Core Library

```python
from prl_bib2html import (
    PublicationsConfig,
    load_projects_config,
    list_publications_by_project
)

# Load configuration
config = PublicationsConfig(
    # ... your config ...
    projects_yaml_path="data/projects.yaml"
)

# Load projects metadata
projects_config = load_projects_config(config.projects_yaml_path)

# Get publications grouped by project
project_pubs = list_publications_by_project(config, projects_config)

# project_pubs is a dict: {"project-name": [Publication, ...], ...}
for project_name, publications in project_pubs.items():
    print(f"{project_name}: {len(publications)} papers")
```

### Flask Application

The Flask demo automatically includes:
- `/publications` route showing all publications with project badges
- `/projects` route showing all projects with their related papers

Run the Flask demo:
```bash
cd demos/flask
uv run python app.py
```

Visit:
- http://127.0.0.1:5000/publications - View publications with project tags
- http://127.0.0.1:5000/projects - View projects with related papers

### Standalone HTML Generator

The HTML generator now creates both publications and projects pages:

```bash
cd demos/html
uv run python generate_html.py
```

This generates:
- `publications.html` - Publications page with project badges
- `projects.html` - Projects page with related papers

## API Reference

### New Functions

#### `load_projects_config(yaml_path: str) -> Dict`
Load projects configuration from YAML file.

**Parameters:**
- `yaml_path`: Path to the projects YAML file

**Returns:**
- Dictionary mapping project names to project metadata

#### `list_publications_by_project(config, projects_config) -> Dict[str, List[Publication]]`
Group publications by project, filtering to only valid projects.

**Parameters:**
- `config`: PublicationsConfig instance
- `projects_config`: Dictionary of project metadata from YAML

**Returns:**
- Dictionary mapping project names to lists of publications

### Updated Classes

#### `PublicationsConfig`
New optional field:
- `projects_yaml_path: Optional[str]` - Path to projects YAML file

#### `Publication`
New field:
- `projects: List[str]` - List of project names this publication belongs to

## Project YAML Schema

```yaml
project-name:
  title: "Project Display Title"
  description: "String describing the project"
  website: "https://project-website-url.com"
  status: "active|archived"
```

**Fields:**
- `title` (optional): Display title for the project (defaults to project-name if not provided)
- `description` (optional): Brief description of the project
- `website` (optional): URL to project website or repository
- `status` (optional): Either "active" or "archived"

## Features by Component

### Publications Page
- Shows project badges for papers with valid projects
- Badges link to the projects page with anchor navigation
- Only displays projects that exist in the YAML configuration

### Projects Page
- Lists all projects from the YAML file
- Shows project metadata (description, website, status)
- Displays status as color-coded badges
- Lists all related publications under each project
- Publications are sorted by year (newest first)

## Migration Guide

For existing installations:

1. **Add PyYAML dependency** (already added to `pyproject.toml`)
   ```bash
   uv pip install -e .
   ```

2. **Create projects.yaml** in your data directory

3. **Add project fields** to BibTeX entries as needed

4. **Update configuration** to include `projects_yaml_path`

5. **No breaking changes**: If you don't specify `projects_yaml_path`, the system works exactly as before

## Example Use Cases

### Single Project Paper
```bibtex
@inproceedings{example2024,
  title = {Example Paper},
  author = {Author, A.},
  year = {2024},
  project = {ada}
}
```

### Multi-Project Paper
```bibtex
@article{collaborative2024,
  title = {Collaborative Research},
  author = {Author, B.},
  year = {2024},
  project = {ada, herbpy, dart}
}
```

### Paper Without Project
```bibtex
@inproceedings{general2024,
  title = {General Paper},
  author = {Author, C.},
  year = {2024}
}
```
Papers without the `project` field or with invalid project names (not in YAML) won't show project badges.

## Notes

- Project names in BibTeX and YAML must match exactly (case-sensitive)
- Multiple projects are comma-separated in the BibTeX `project` field
- Only projects defined in the YAML file will be displayed
- If `projects_yaml_path` is not specified or the file doesn't exist, the system gracefully handles it with no errors

