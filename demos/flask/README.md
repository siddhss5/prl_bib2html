# Flask Demo

A minimal Flask web application that serves publications, people, and projects pages from labdata output.

## Usage

```bash
cd demos/flask
pip install flask
python app.py
```

Then visit:
- http://127.0.0.1:5000/publications
- http://127.0.0.1:5000/people
- http://127.0.0.1:5000/projects

## How It Works

The app calls `assemble()` once at startup to load all data, then passes it to Jinja2 templates for rendering. This means the data is assembled once and served from memory on each request.

```python
from labdata import LabDataConfig, assemble

config = LabDataConfig.from_yaml("config.yaml")
DATA = assemble(config)
```

## Configuration

Edit `config.yaml` to point to your own data. You can also set the config path via environment variable:

```bash
CONFIG_FILE=my_config.yaml python app.py
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask application |
| `config.yaml` | labdata configuration |
| `templates/` | Jinja2 templates (publications, people, projects) |
