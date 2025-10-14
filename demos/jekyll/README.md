# Jekyll Data Generator Demo

This demo shows how to generate Jekyll-compatible YAML data files from BibTeX sources for use with Jekyll-based sites (like GitHub Pages with Minimal Mistakes theme).

## Overview

Instead of generating complete HTML files, this approach:
1. ✅ Generates YAML data files that Jekyll can read
2. ✅ Uses Jekyll's Liquid templating to render pages
3. ✅ Automatically inherits Minimal Mistakes styling
4. ✅ Stays fully within the Jekyll/GitHub Pages ecosystem

## Quick Start

### 1. Generate Data Files

```bash
cd demos/jekyll
uv run python generate_jekyll_data.py
```

This creates in the current directory:
- `publications.yml`
- `projects.yml`

The demo uses the shared data directory at `../../data/` (same as Flask and HTML demos).

### 2. Copy to Your Jekyll Site

Copy the generated files and templates to your Jekyll site:

```bash
# Copy data files
cp publications.yml <your-jekyll-site>/_data/
cp projects.yml <your-jekyll-site>/_data/

# Copy page templates
cp publications_template.md <your-jekyll-site>/_pages/publications.md
cp projects_template.md <your-jekyll-site>/_pages/projects.md
```

### 3. Add Projects to Navigation

Edit `<your-jekyll-site>/_data/navigation.yml`:

```yaml
main:
  - title: "CV"
    url: /cv/
  - title: "Contact"
    url: /contact/
  - title: "Publications"
    url: /publications/
  - title: "Projects"        # ADD THIS
    url: /projects/          # ADD THIS
  - title: "Teaching"
    url: /teaching/
  - title: "Posts"
    url: /posts/
  - title: "Categories"
    url: /categories/
  - title: "Tags"
    url: /tags/
```

### 4. Test Locally

```bash
cd <your-jekyll-site>
bundle exec jekyll serve
```

Visit: http://localhost:4000/publications/ and http://localhost:4000/projects/

### 5. Deploy

```bash
cd <your-jekyll-site>
git add _data/ _pages/ 
git commit -m "Add project-based publication organization"
git push
```

GitHub Pages will automatically rebuild and deploy!

## Workflow for Updates

When you add new publications or update projects:

```bash
# 1. Update your BibTeX files or projects YAML
# Edit your publication files or projects configuration

# 2. Regenerate Jekyll data
cd demos/jekyll
uv run python generate_jekyll_data.py

# 3. Copy to your Jekyll site
cp publications.yml projects.yml <your-jekyll-site>/_data/

# 4. Commit and push
cd <your-jekyll-site>
git add _data/
git commit -m "Update publications and projects data"
git push
```

For your personal site, you can modify `config.yaml` to point to your own BibTeX sources and projects configuration.

## Generated Data Structure

### publications.yml

```yaml
2025:
  Journal Papers:
    - title: "Paper Title"
      authors: "A. Author and B. Author"
      venue: "Journal Name, 2025"
      year: 2025
      pdf_url: "https://..."
      note: "Award info"
      projects: ["project1", "project2"]
      entry_type: "Journal Papers"
  Conference Papers:
    - title: "..."
      # ...
2024:
  # ...
```

### projects.yml

```yaml
robotfeeding:
  title: "Robot-Assisted Feeding"
  description: "Project description"
  website: "https://robotfeeding.io"
  status: "active"
  publications:
    - title: "..."
      authors: "..."
      # ... (same structure as above)
```

## Customization

### Styling

The template pages use inline styles that work with Minimal Mistakes. You can customize:

- Button styles: `btn--info`, `btn--success`, `btn--secondary`, `btn--primary`
- Notices: `notice`, `notice--info`, `notice--warning`
- Layout: `layout: single`, `classes: wide`

### Templates

Edit the template files to change:
- Publication formatting
- Project card layout
- Header images
- Additional metadata display

### Configuration

Edit `generate_jekyll_data.py` to change:
- BibTeX source URLs
- Jekyll site path
- Project sort order
- Data structure

## Advantages of This Approach

1. **Full Jekyll Integration**: Pages render with Jekyll, inherit all theme features
2. **GitHub Pages Compatible**: No external build step required
3. **Easy Updates**: Just run one Python script and push
4. **Flexible Templating**: Use Liquid to customize rendering
5. **Automatic Styling**: Minimal Mistakes theme applied automatically
6. **Fast Builds**: Jekyll only rebuilds when data changes

## Troubleshooting

### Projects not showing
1. Ensure project names in BibTeX match YAML exactly
2. Run generator script to update data files
3. Check that `projects.yml` was created
4. Verify you copied it to your Jekyll site's `_data/` directory

### Styling looks off
1. Check that you're using `layout: single` and `classes: wide` in the page templates
2. Verify button class names match Minimal Mistakes: `btn--info`, `btn--primary`, etc.
3. Test locally with `bundle exec jekyll serve`

### Output files not found
The generator outputs to the `demos/jekyll/` directory. Check there for the generated `.yml` files.

## Files in This Directory

- `generate_jekyll_data.py` - Main generator script
- `publications_template.md` - Example publications page for Jekyll
- `projects_template.md` - Example projects page for Jekyll
- `README.md` - This file

## Next Steps

1. Run the generator: `python generate_jekyll_data.py`
2. Review the generated YAML files
3. Copy templates to your Jekyll site
4. Test locally
5. Deploy to GitHub Pages

For questions or issues, see the main project README or PROJECTS_FEATURE.md.

