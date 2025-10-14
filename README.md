# prl-bib2html

A Python library for converting BibTeX files to HTML for academic publications websites.

## Overview

`prl-bib2html` is a lightweight Python library that transforms BibTeX publication files into clean, categorized HTML output. It's designed for academic labs and researchers who want to display their publications on websites with professional formatting.

## Features

- **📚 BibTeX Processing**: Parse and format BibTeX files with rich academic metadata
- **🌐 Remote Sources**: Fetch BibTeX files from remote repositories (GitHub, GitLab, etc.)
- **📄 PDF Integration**: Support for both local and remote PDF links
- **🎨 LaTeX Support**: Convert LaTeX formatting, accents, and math expressions to HTML
- **👥 Author Formatting**: Intelligent author name formatting and abbreviation
- **📅 Year Grouping**: Automatic organization by publication year and type
- **🔗 URL Support**: Handle publication URLs, video links, and external resources
- **📁 Project Organization**: Group publications by research projects with YAML-based metadata
- **⚡ Framework Agnostic**: Use with any web framework or standalone

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

### Development Installation (Recommended)

Since this package is not yet published to PyPI, you need to install it from the local repository:

```bash
# Clone the repository
git clone https://github.com/personalrobotics/prl_bib2html.git
cd prl_bib2html

# Create and activate virtual environment (uv handles this automatically)
uv venv

# Install in development mode with demo support
uv pip install -e ".[demo]"
```

**Note**: `uv` automatically creates and manages virtual environments. If you're using `pip`, you'll need to create a virtual environment manually:

```bash
# Alternative: Using pip with manual venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -e ".[demo]"
```

### Core Library Only

```bash
# Install just the core library (no Flask)
uv pip install -e .
```

### Future PyPI Installation

Once the package is published to PyPI, you'll be able to install it directly:

```bash
# Core library
uv pip install prl-bib2html

# With demo support
uv pip install "prl-bib2html[demo]"
```

## Quick Start

### Using the CLI (Easiest)

```bash
# 1. Create a config.yaml file
cat > config.yaml << EOF
bibtex:
  source_url: "https://raw.githubusercontent.com/your-repo/pubs/main"
  cache_dir: "data/bib"
  files:
    - name: "journal.bib"
      category: "Journal Papers"
    - name: "conference.bib"
      category: "Conference Papers"

output:
  pdf_base_url: "https://your-site.com/pdfs"
EOF

# 2. Generate data
prl-bib2html --config config.yaml --format yaml --output publications.yml

# Now use publications.yml in your templating system!
```

### Using the Python API

```python
from prl_bib2html import LibraryConfig, list_publications, export_to_yaml

# Load from YAML config file
config = LibraryConfig.from_yaml("config.yaml")

# Generate publications data
publications = list_publications(config.to_publications_config())

# Export to YAML or JSON
export_to_yaml(publications, "publications.yml")
# Or: export_to_json(publications, "publications.json")
```

### Legacy API (Still Supported)

The original API still works for backward compatibility:

```python
from prl_bib2html import PublicationsConfig, list_publications

config = PublicationsConfig(
    bibtex_base_url="https://raw.githubusercontent.com/your-repo/pubs/main",
    bibtex_cache_dir="data/bib",
    pdf_base_dir="https://your-domain.com/pdfs",
    bib_files=[
        ("journal.bib", "Journal Papers"),
        ("conference.bib", "Conference Papers"),
    ]
)

publications = list_publications(config)
# {2024: {"Journal Papers": [Publication, ...], ...}, ...}
```

## Demos

The project includes three demonstration applications showing different ways to consume the generated data.

### 1. Standalone HTML Generator

**Location**: `demos/html/`

Generate complete, self-contained HTML pages with Bootstrap styling.

```bash
cd demos/html
uv run python generate_html.py
```

**What it demonstrates:**
- Loading config from `config.yaml`
- Generating static HTML pages from publication data
- Bootstrap-based responsive design

**Output**: `publications.html` and `projects.html`

### 2. Flask Web Application

**Location**: `demos/flask/`

A dynamic Flask web application serving publication data.

```bash
cd demos/flask
uv run python app.py
```

**What it demonstrates:**
- Loading config from `config.yaml`
- Using publication data in a web framework
- Jinja2 templating with live data

**Access**: 
- http://127.0.0.1:5000/publications
- http://127.0.0.1:5000/projects

### 3. Jekyll/GitHub Pages Generator

**Location**: `demos/jekyll/`

Generate Jekyll-compatible YAML data files for GitHub Pages sites.

```bash
cd demos/jekyll
uv run python generate_jekyll_data.py
```

**What it demonstrates:**
- Generating data files for Jekyll's Liquid templating
- Integration with Minimal Mistakes theme
- Workflow for static site generators

**Output**: `_data/publications.yml` and `_data/projects.yml` in your Jekyll site

## Configuration

### Configuration File (Recommended)

Create a `config.yaml` file to configure the library:

```yaml
bibtex:
  source_url: "https://raw.githubusercontent.com/your-repo/pubs/main"
  cache_dir: "data/bib"
  files:
    - name: "journal.bib"
      category: "Journal Papers"
    - name: "conference.bib"
      category: "Conference Papers"

projects:
  config_file: "data/projects-config.yaml"

output:
  pdf_base_url: "https://your-site.com/pdfs"
```

Then use it with the CLI:
```bash
prl-bib2html --config config.yaml --output publications.yml
```

Or in Python:
```python
from prl_bib2html import LibraryConfig

config = LibraryConfig.from_yaml("config.yaml")
```

### CLI Usage

```bash
# Generate YAML output (default)
prl-bib2html --config config.yaml --output publications.yml

# Generate JSON output
prl-bib2html --config config.yaml --format json --output publications.json

# Generate both publications and projects to a directory
prl-bib2html --config config.yaml --output-dir _data/

# Generate only publications
prl-bib2html --config config.yaml --publications-only --output pubs.yml

# Generate only projects
prl-bib2html --config config.yaml --projects-only --output projects.yml
```

### PublicationsConfig (Legacy)

The original configuration class still works for backward compatibility:

```python
@dataclass
class PublicationsConfig:
    bibtex_base_url: str           # Base URL for BibTeX files
    bibtex_cache_dir: str          # Local cache directory
    pdf_base_dir: str              # Base directory/URL for PDFs (supports both local paths and URLs)
    bib_files: List[tuple]         # List of (filename, display_name) tuples
    projects_yaml_path: Optional[str]  # Optional path to projects YAML file
```

### Environment Variables

**Flask Demo Only**: The Flask demo supports configuration via environment variables:

```bash
export BIBTEX_BASE_URL="https://raw.githubusercontent.com/your-repo/pubs/main"
export BIBTEX_CACHE_DIR="data/bib"
export PDF_BASE_DIR="https://your-domain.com/pdfs"
```

**Standalone HTML Demo**: Uses hardcoded configuration in `generate_html.py`.

### PDF Base Directory

The `pdf_base_dir` supports both local paths and URLs:

- **Local Path**: `"data/pdf"` - checks if files exist locally
- **URL**: `"https://example.com/pdfs"` - constructs direct URLs

## API Reference

### Core Functions

#### `list_publications(config: PublicationsConfig) -> dict`

Processes BibTeX files and returns publications organized by year and category.

**Returns**: `{year: {category: [Publication, ...], ...}, ...}`

#### `load_projects_config(yaml_path: str) -> dict`

Load project metadata from a YAML configuration file.

**Returns**: Dictionary mapping project names to project metadata

#### `list_publications_by_project(config: PublicationsConfig, projects_config: dict) -> dict`

Group publications by project, filtering to only valid projects defined in the YAML.

**Returns**: `{project_name: [Publication, ...], ...}`

#### `PublicationsConfig`

Configuration class for the library.

### Data Classes

#### `Publication`

```python
@dataclass
class Publication:
    entry_type: str           # Publication category
    year: int                 # Publication year
    title: str                # Formatted title with HTML
    authors: str              # Formatted author list
    venue: str                # Journal/conference name
    note: str                 # Additional notes/links
    pdf_url: Optional[str]    # PDF link if available
    projects: List[str]       # List of associated project names
```

## Advanced Features

### LaTeX Support

The library automatically converts:
- LaTeX accents (é, ü, ñ, etc.)
- Mathematical expressions
- Bold and italic formatting
- Superscripts and subscripts
- Hyperlinks

### Author Formatting

Author names are intelligently formatted:
- "Last, First" → "F. Last"
- Multiple authors with proper "and" conjunctions
- Affiliation superscripts preserved
- Special characters handled

### Caching

BibTeX files are automatically cached locally to improve performance and reduce network requests.

### Project Organization

Organize publications by research projects using BibTeX tags and YAML metadata:

1. **Add project tags to BibTeX entries:**
   ```bibtex
   @inproceedings{smith2024,
     title = {My Paper},
     author = {Smith, J.},
     year = {2024},
     project = {robotics, ml}  # Can specify multiple projects
   }
   ```

2. **Create `data/projects-config.yaml`:**
   ```yaml
   robotics:
     title: "Robotics Research"
     description: "Advanced robotics systems"
     website: "https://example.com/robotics"
     status: "active"
   
   ml:
     title: "Machine Learning"
     description: "ML for robotics"
     website: "https://example.com/ml"
     status: "archived"
   ```

3. **Projects are automatically:**
   - Displayed on dedicated `/projects` page
   - Shown as badges on publications page
   - Sorted by status (active first), newest publication, then alphabetically

For detailed documentation, see [PROJECTS_FEATURE.md](PROJECTS_FEATURE.md).

## Project Structure

```
prl_bib2html/
├── prl_bib2html/           # Core library
│   ├── __init__.py
│   └── publications.py
├── demos/                  # Demonstration applications
│   ├── html/              # Standalone HTML generator
│   │   ├── generate_html.py
│   │   └── README.md
│   └── flask/             # Flask web application
│       ├── app.py
│       └── templates/
├── data/                  # Cached BibTeX files
├── pyproject.toml         # Project configuration
└── README.md
```

## Dependencies

### Core Dependencies
- `bibtexparser` - BibTeX parsing
- `requests` - HTTP requests for remote files
- `pyyaml` - YAML parsing for project metadata

### Optional Dependencies
- `Flask` - Web framework (for Flask demo)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington