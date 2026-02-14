# Examples

Simple examples demonstrating how to use labdata.

## Files

- `config.yaml` - Example configuration file
- `basic_usage.py` - Python API examples

## Quick Start

### Using the CLI

```bash
# 1. Copy and customize the example config
cp examples/config.yaml myconfig.yaml
# Edit myconfig.yaml with your settings

# 2. Generate YAML output
labdata --config myconfig.yaml --format yaml --output publications.yml

# 3. Generate JSON output
labdata --config myconfig.yaml --format json --output publications.json

# 4. Generate both publications and projects
labdata --config myconfig.yaml --output-dir _data/
```

### Using the Python API

```python
from labdata import LibraryConfig, list_publications, export_to_yaml

# Load config
config = LibraryConfig.from_yaml("config.yaml")

# Generate publications
pubs = list_publications(config.to_publications_config())

# Export to YAML
export_to_yaml(pubs, "publications.yml")
```

## Configuration File Format

See `config.yaml` for a complete annotated example.

## More Complex Examples

For full-featured examples with web frameworks and templates, see the `demos/` directory:

- `demos/flask/` - Flask web application
- `demos/html/` - Static HTML generator  
- `demos/jekyll/` - Jekyll/GitHub Pages generator

