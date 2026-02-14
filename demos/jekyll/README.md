# Jekyll Demo

Generate a `lab.yml` data file from BibTeX, then render it in Jekyll using the included Liquid templates.

## Usage

```bash
cd demos/jekyll
python generate_jekyll_data.py
```

This produces `lab.yml` containing all publications, people, and projects.

## Integrating with Your Jekyll Site

**1. Copy the data file:**

```bash
cp lab.yml <your-jekyll-site>/_data/
```

**2. Copy the page templates:**

```bash
cp publications_template.md <your-jekyll-site>/_pages/publications.md
cp projects_template.md <your-jekyll-site>/_pages/projects.md
```

**3. Add navigation** (in `_data/navigation.yml`):

```yaml
main:
  - title: "Publications"
    url: /publications/
  - title: "Projects"
    url: /projects/
```

**4. Test locally:**

```bash
cd <your-jekyll-site>
bundle exec jekyll serve
```

## Updating Publications

When you add new BibTeX entries or update your YAML files:

```bash
cd demos/jekyll
python generate_jekyll_data.py
cp lab.yml <your-jekyll-site>/_data/
cd <your-jekyll-site>
git add _data/lab.yml && git commit -m "Update publications" && git push
```

## Configuration

Edit `config.yaml` to point to your own BibTeX and YAML files:

```yaml
bib_dir: "path/to/your/bib"
bib_files:
  - name: "journal.bib"
    category: "Journal Papers"
  - name: "conference.bib"
    category: "Conference Papers"

pdf_base_url: "https://your-lab.edu/pdfs"
people_file: "path/to/people.yaml"
projects_file: "path/to/projects.yaml"
```

## Template Customization

The included templates (`publications_template.md`, `projects_template.md`) are designed for the Minimal Mistakes theme but can be adapted to any Jekyll theme. They access data from `site.data.lab.publications`, `site.data.lab.people`, and `site.data.lab.projects`.

## Files

| File | Purpose |
|------|---------|
| `generate_jekyll_data.py` | Runs labdata and writes `lab.yml` |
| `config.yaml` | labdata configuration (BibTeX paths, etc.) |
| `publications_template.md` | Jekyll page template for publications |
| `projects_template.md` | Jekyll page template for projects |
