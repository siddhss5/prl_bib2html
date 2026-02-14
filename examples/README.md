# Examples

Simple examples demonstrating how to use labdata.

## Files

- `config.yaml` - Example configuration file
- `basic_usage.py` - Python API examples

## Quick Start

### Using the CLI

```bash
# Generate YAML output
labdata --config config.yaml --output lab.yml

# Generate JSON output
labdata --config config.yaml --format json --output lab.json

# Validate configuration and see data summary
labdata --config config.yaml --validate

# Show unresolved author names
labdata --config config.yaml --unresolved
```

### Using the Python API

```python
from labdata import LabDataConfig, assemble, export_to_yaml

config = LabDataConfig.from_yaml("config.yaml")
data = assemble(config)
export_to_yaml(data, "lab.yml")

# Access the data
for pub in data.publications:
    print(pub.title, [a.name for a in pub.authors])
```

## Configuration File Format

See `config.yaml` for a complete annotated example.

## More Complex Examples

For full-featured examples with web frameworks and templates, see the `demos/` directory:

- `demos/flask/` - Flask web application
- `demos/html/` - Static HTML generator
- `demos/jekyll/` - Jekyll/GitHub Pages generator
