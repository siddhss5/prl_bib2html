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

```python
from prl_bib2html import PublicationsConfig, list_publications

# Configure your BibTeX sources
config = PublicationsConfig(
    bibtex_base_url="https://raw.githubusercontent.com/your-repo/pubs/main",
    bibtex_cache_dir="data/bib",
    pdf_base_dir="https://your-domain.com/pdfs",
    bib_files=[
        ("journal.bib", "Journal Papers"),
        ("conference.bib", "Conference Papers"),
        ("other.bib", "Other Papers"),
    ]
)

# Generate publications data
publications = list_publications(config)

# publications is now a dict organized by year and category
# {2024: {"Journal Papers": [Publication, ...], ...}, ...}
```

## Demos

The project includes two demonstration applications showing different ways to use the library.

### 1. Standalone HTML Generator

**Location**: `demos/html/`

Generate a complete HTML publications page without any web framework.

```bash
cd demos/html
uv run python generate_html.py
```

**Features**:
- ✅ No web framework required
- ✅ Complete HTML page with CSS styling
- ✅ Responsive design
- ✅ Direct PDF links
- ✅ Professional academic styling

**Output**: Generates `publications.html` that you can open directly in any browser or host on any static file server.

### 2. Flask Web Application

**Location**: `demos/flask/`

A complete Flask web application demonstrating the library in a web framework.

```bash
cd demos/flask
uv run python app.py
```

**Features**:
- ✅ Full web application with routing
- ✅ Template-based rendering
- ✅ Auto-redirect to publications page
- ✅ Development server with hot reload

**Access**: http://127.0.0.1:5000

## Configuration

### PublicationsConfig

The main configuration class that controls how the library works:

```python
@dataclass
class PublicationsConfig:
    bibtex_base_url: str      # Base URL for BibTeX files
    bibtex_cache_dir: str     # Local cache directory
    pdf_base_dir: str         # Base directory/URL for PDFs (supports both local paths and URLs)
    bib_files: List[tuple]    # List of (filename, display_name) tuples
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