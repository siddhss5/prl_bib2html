# Static HTML Demo

Generate a standalone HTML publications page from BibTeX. No web framework required.

## Usage

```bash
cd demos/html
python generate_html.py
```

This produces `publications.html`, which you can open directly in a browser.

## How It Works

The script calls `assemble()` to build the full dataset, then iterates through publications to generate HTML with Bootstrap styling. This demonstrates how to write a custom renderer on top of labdata's structured output.

## Configuration

Edit `config.yaml` to point to your own BibTeX files:

```yaml
bib_dir: "path/to/your/bib"
bib_files:
  - name: "journal.bib"
    category: "Journal Papers"

pdf_base_url: "https://your-lab.edu/pdfs"
```

## Files

| File | Purpose |
|------|---------|
| `generate_html.py` | HTML page generator |
| `config.yaml` | labdata configuration |
