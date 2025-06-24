# Personal Robotics Lab Publication Website

This project automatically converts BibTeX publication files into a clean, categorized, and searchable HTML website. It is optimized for rendering academic publications with rich formatting (LaTeX, superscripts, awards, and video links) and supports automatic grouping by year and publication type.

## Features

- **Publication Organization**: Automatically categorizes publications by year and type (Journal Papers, Conference Papers, Other Papers)
- **LaTeX Support**: Renders LaTeX math expressions and formatting in publication titles and content
- **PDF Links**: Direct links to PDF files when available
- **Author Formatting**: Properly formats author names with initials and affiliations
- **Responsive Design**: Bootstrap-based responsive layout
- **Math Rendering**: KaTeX integration for beautiful mathematical notation display

## Project Structure

```
prl-pubsite/
├── app.py                 # Main Flask application
├── publications.py        # Publication parsing and formatting logic
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── templates/
│   ├── base.html         # Base template with navigation
│   └── publications.html # Publications display template
└── data/
    └── pubs/             # Cached BibTeX files
```

## Setup

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
uv pip install .
```

This installs the project and dependencies using `pyproject.toml`.

### Run the Development Server

Simply run the app directly using `uv`:

```bash
uv python app.py
```

The application will be available at:
- **Main page**: http://localhost:5000/
- **Publications page**: http://localhost:5000/publications

### Development Mode

The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Debugger interface

## Configuration

### Environment Variables

- `PRL_PUBS`: Path to the publications directory containing PDF files (defaults to `/cse/web/research/personalroboticslab/personalrobotics/publications/`)

### BibTeX Sources

The application fetches publication data from the following BibTeX files:
- `siddpubs-journal.bib` - Journal Papers
- `siddpubs-conf.bib` - Conference Papers  
- `siddpubs-misc.bib` - Other Papers

These files are automatically downloaded from the [personalrobotics/pubs](https://github.com/personalrobotics/pubs) repository and cached locally.

## Features in Detail

### Publication Parsing

The `publications.py` module handles:
- BibTeX parsing with `bibtexparser`
- LaTeX accent and formatting conversion
- Author name normalization and abbreviation
- Publication type detection and formatting
- PDF file availability checking

### LaTeX Support

The application supports:
- Mathematical expressions (rendered with KaTeX)
- LaTeX accents (é, ü, etc.)
- Bold and italic formatting
- Superscripts and subscripts
- Hyperlinks

### Author Formatting

Author names are automatically:
- Converted from "Last, First" to "F. Last" format
- Handled for multiple authors with proper "and" conjunctions
- Preserved with affiliations and superscripts

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for fetching BibTeX files
- **bibtexparser**: BibTeX parsing library
- **Bootstrap**: CSS framework for styling
- **KaTeX**: Math rendering library
