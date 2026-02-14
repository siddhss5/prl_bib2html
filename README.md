# labdata

A data assembler for academic lab websites. Turns BibTeX files and simple YAML into structured, cross-referenced data that any site generator can consume.

## The Problem

Every academic lab maintains BibTeX files. Building a website from them means writing custom scripts that break whenever the data format changes, duplicating author metadata across files, and manually keeping publication pages in sync with project pages.

## What labdata Does

labdata reads your existing BibTeX files, combines them with optional YAML files for people and projects, and outputs a single structured YAML or JSON file with all cross-references resolved:

- Publication authors are matched to lab members (via configurable aliases and fuzzy matching)
- Publications are linked to research projects (via BibTeX `project` tags)
- People and projects get back-linked lists of their publications
- LaTeX formatting is converted to Markdown (not HTML), so any renderer can consume it

The output works with Jekyll, Hugo, Flask, Eleventy, React, or anything else that reads YAML/JSON.

## Installation

```bash
git clone https://github.com/siddhss5/labdata.git
cd labdata
pip install -e .
```

## Quick Start

**1. Create a configuration file** (`lab.yaml`):

```yaml
lab:
  name: "My Lab"
  description: "What our lab does"
  university: "University Name"
  website: "https://mylab.edu"

bib_dir: "data/bib"
bib_files:
  - name: "journal.bib"
    category: "Journal Papers"
  - name: "conference.bib"
    category: "Conference Papers"

pdf_base_url: "https://your-lab.edu/pdfs"
people_file: "data/people.yaml"       # optional
projects_file: "data/projects.yaml"   # optional
```

**2. Run it:**

```bash
labdata --config lab.yaml --output lab.yml
```

**3. Check your data quality:**

```bash
# Summary and validation
labdata --config lab.yaml --validate

# List author names that couldn't be matched to lab members
labdata --config lab.yaml --unresolved
```

## Input Files

### BibTeX Files

Standard `.bib` files. Tag publications with projects using a `project` field:

```bibtex
@inproceedings{nanavati2025lessons,
  title   = {Lessons Learned from Robot-assisted Feeding},
  author  = {Nanavati, Amal and Srinivasa, Siddhartha},
  year    = {2025},
  project = {robotfeeding}
}
```

### People (`data/people.yaml`)

A list of lab members and alumni. The `aliases` field is how labdata matches BibTeX author names to people:

```yaml
- id: "nanavati"
  name: "Amal Nanavati"
  aliases: ["A. Nanavati", "A. M. Nanavati"]
  role: "phd_student"
  status: "current"
  website: "https://amaln.com"

- id: "jdoe"
  name: "Jane Doe"
  aliases: ["J. Doe", "J. A. Doe"]
  role: "phd_student"
  status: "alumni"
  end_year: 2023
  degree: "PhD"
  thesis_title: "Adaptive Robot Manipulation"
  current_position: "Research Scientist at Google"
```

### Projects (`data/projects.yaml`)

```yaml
- id: "robotfeeding"
  title: "Robot-Assisted Feeding"
  description: "Autonomous feeding for people with mobility impairments"
  website: "https://robotfeeding.io"
  status: "active"
```

## Output

A single YAML (or JSON) file with three sections:

```yaml
publications:
  - bib_id: "nanavati2025lessons"
    title: "Lessons Learned from Robot-assisted Feeding"
    authors:
      - name: "A. Nanavati"
        person_id: "nanavati"       # matched to people.yaml
      - name: "S. Srinivasa"
        person_id: null             # external collaborator
    year: 2025
    venue: "*HRI*, 2025"            # Markdown formatting
    category: "Conference Papers"
    pdf_url: "https://your-lab.edu/pdfs/nanavati2025lessons.pdf"
    doi_url: "https://doi.org/10.1234/..."
    project_ids: ["robotfeeding"]

people:
  - id: "nanavati"
    name: "Amal Nanavati"
    role: "phd_student"
    status: "current"
    publication_count: 12
    publication_ids: ["nanavati2025lessons", ...]   # auto-computed

projects:
  - id: "robotfeeding"
    title: "Robot-Assisted Feeding"
    status: "active"
    publication_ids: ["nanavati2025lessons", ...]   # auto-computed
    people_ids: ["nanavati", ...]                   # auto-computed
```

## Python API

```python
from labdata import LabDataConfig, assemble, export_to_yaml

config = LabDataConfig.from_yaml("lab.yaml")
data = assemble(config)

# Export to file
export_to_yaml(data, "lab.yml")

# Or work with the data directly
for pub in data.publications:
    authors = ", ".join(a.name for a in pub.authors)
    print(f"{pub.title} ({authors})")

for person in data.people:
    print(f"{person.name}: {person.publication_count} publications")
```

## Site

The [`site/`](site/) directory contains a complete Jekyll site using the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme. It renders publications, people, and projects pages from labdata output.

**To use it with your own data:**

1. Fork this repo
2. Edit `lab.yaml` to point to your BibTeX files
3. Enable GitHub Pages (Settings → Pages → Source: GitHub Actions)
4. Push — the site builds and deploys automatically

**To preview locally:**

```bash
labdata --config lab.yaml --output site/_data/lab.yml
cd site && bundle install && bundle exec jekyll serve
```

The GitHub Actions workflow in `.github/workflows/deploy.yml` runs `labdata` to generate `site/_data/lab.yml`, then builds and deploys the Jekyll site to GitHub Pages.

## How Author Matching Works

labdata uses a two-pass strategy to match BibTeX author names to lab members:

1. **Exact alias match**: Checks each author name against the `aliases` list in `people.yaml` (after normalizing case, accents, and punctuation)
2. **Fuzzy fallback**: Uses string similarity (threshold: 0.85) to catch minor spelling variations

Authors who don't match anyone in `people.yaml` are left with `person_id: null`. Use `labdata --unresolved` to review them.

## Dependencies

- **bibtexparser** - BibTeX parsing
- **pyyaml** - YAML I/O

No network calls. All processing is local and offline.

## License

MIT License. Copyright (c) 2024 Personal Robotics Laboratory, University of Washington.
