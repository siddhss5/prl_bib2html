# labdata

Most academic lab websites are a mess. Publications are added by hand, people pages go stale, and project links rot. Updating the site becomes one more chore that nobody wants to do, so it falls behind.

However, most academics already maintain excellent, up-to-date BibTeX files. labdata turns that BibTeX into a website. Add one custom tag (`project`) to your entries and labdata auto-generates publications, people, and project pages with full cross-referencing.

## How It Works

1. **Fork this repo**
2. **Drop in your `.bib` files** and edit `lab.yaml` with your lab's info
3. **Enable GitHub Pages** (Settings → Pages → Source: GitHub Actions)
4. **Push** — your site builds and deploys automatically

That's it. Every time you push updated BibTeX, the site regenerates. No manual HTML editing, no copy-paste errors, no drift between your papers and your website.

**[See a live example →](https://goodrobot.ai/labdata/)**

## What You Get

- **Publications page** with search, collapsible abstracts, BibTeX copy buttons, and DOI/arXiv links
- **People page** with current members, alumni, and 350+ collaborators — all auto-detected from paper co-authorship
- **Projects page** with linked publications (tag papers in BibTeX with `project = {myproject}`)
- **Landing page** with your lab name, description, and links

The site uses the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) Jekyll theme and deploys to GitHub Pages for free.

## Setup

### 1. Fork and clone

```bash
git clone https://github.com/YOUR-USERNAME/labdata.git
cd labdata
pip install -e .
```

### 2. Configure `lab.yaml`

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

### 3. Add your data

- Put your `.bib` files in `data/bib/`
- Optionally create `data/people.yaml` for lab members (see below)
- Optionally create `data/projects.yaml` for research projects (see below)

### 4. Preview locally

```bash
labdata --config lab.yaml --output site/_data/lab.yml
cd site && bundle install && bundle exec jekyll serve
```

### 5. Deploy

Enable GitHub Pages in your repo settings (Source: GitHub Actions) and push. The included workflow generates the site data and deploys automatically.

## Data Files

### BibTeX (required)

Standard `.bib` files. labdata extracts the following standard BibTeX fields:

| Field | Used for |
|-------|----------|
| `title` | Publication title (LaTeX converted to Markdown) |
| `author` | Author list (auto-matched to lab members) |
| `year` | Sorting and grouping |
| `booktitle` / `journal` | Venue display |
| `doi` | DOI link button |
| `eprint` + `archivePrefix` | arXiv link button |
| `abstract` | Collapsible abstract panel |
| `note` | Highlighted note (e.g. "Best Paper Award") |
| `url` | Video link (if YouTube/Vimeo) or generic link |

All fields are also preserved in the copyable BibTeX button.

### The `project` tag

labdata introduces one custom BibTeX field: `project`. Add it to any entry to link that paper to a research project:

```bibtex
@inproceedings{nanavati2025lessons,
  title    = {Lessons Learned from Robot-assisted Feeding},
  author   = {Nanavati, Amal and Srinivasa, Siddhartha},
  year     = {2025},
  doi      = {10.1234/hri.2025.001},
  abstract = {We present lessons from deploying...},
  note     = {Best Paper Award},
  project  = {robotfeeding}
}
```

This single tag is all labdata needs to auto-generate project pages with linked publications and contributing authors. You can assign multiple projects with commas: `project = {robotfeeding, assistive}`.

### People (optional, `data/people.yaml`)

A list of lab members and alumni. The `aliases` field tells labdata how to match BibTeX author names to people:

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

### Projects (optional, `data/projects.yaml`)

```yaml
- id: "robotfeeding"
  title: "Robot-Assisted Feeding"
  description: "Autonomous feeding for people with mobility impairments"
  website: "https://robotfeeding.io"
  status: "active"
```

## Validation

```bash
# Check data quality
labdata --config lab.yaml --validate

# List author names that couldn't be matched to lab members
labdata --config lab.yaml --unresolved
```

## How Author Matching Works

labdata matches BibTeX author names to lab members in two passes:

1. **Exact alias match** — checks against the `aliases` list in `people.yaml` (after normalizing case, accents, and punctuation)
2. **Fuzzy fallback** — uses string similarity (threshold: 0.85) to catch minor spelling variations

Anyone not matched is listed as a collaborator. Use `labdata --unresolved` to review unmatched names and add aliases as needed.

## Python API

If you want to use labdata programmatically instead of (or in addition to) the Jekyll site:

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
```

The output is a single YAML/JSON file that works with Jekyll, Hugo, Flask, Eleventy, React, or anything else.

## Dependencies

- **bibtexparser** — BibTeX parsing
- **pyyaml** — YAML I/O

No network calls. All processing is local and offline.

## License

MIT License. Copyright (c) 2024 Personal Robotics Laboratory, University of Washington.
