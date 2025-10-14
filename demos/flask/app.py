"""
Flask web application demo for prl_bib2html.

This demo shows how to use the prl_bib2html library in a Flask web application
to display publications on a website.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import os
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from prl_bib2html import (
    LibraryConfig,
    list_publications,
    load_projects_config,
    list_publications_by_project
)

app = Flask(__name__, template_folder='templates')

# Load configuration from YAML file
CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.yaml")
CONFIG_PATH = Path(__file__).parent / CONFIG_FILE

# Load configuration
config = LibraryConfig.from_yaml(str(CONFIG_PATH))
PRL_CONFIG = config.to_publications_config()

@app.route("/")
def index():
    return redirect(url_for('publications'))

@app.route("/publications")
def publications():
    pubs = list_publications(PRL_CONFIG)
    projects_config = load_projects_config(PRL_CONFIG.projects_yaml_path) if PRL_CONFIG.projects_yaml_path else {}
    return render_template("publications.html", pubs=pubs, projects_config=projects_config)

@app.route("/projects")
def projects():
    projects_config = load_projects_config(PRL_CONFIG.projects_yaml_path) if PRL_CONFIG.projects_yaml_path else {}
    project_pubs = list_publications_by_project(PRL_CONFIG, projects_config)
    
    # Sort projects: active first, then by newest publication, then alphabetically
    def project_sort_key(item):
        project_name, project_info = item
        # Status priority: active=0, archived=1, other=2
        status = project_info.get('status', '').lower()
        status_priority = {'active': 0, 'archived': 1}.get(status, 2)
        
        # Get newest publication year (or 0 if no publications)
        newest_year = 0
        if project_name in project_pubs and project_pubs[project_name]:
            newest_year = max(pub.year for pub in project_pubs[project_name])
        
        # Return tuple: (status_priority, -newest_year for descending, project_name)
        return (status_priority, -newest_year, project_name)
    
    sorted_projects = dict(sorted(projects_config.items(), key=project_sort_key))
    
    return render_template("projects.html", projects_config=sorted_projects, project_pubs=project_pubs)

if __name__ == "__main__":
    app.run(debug=True)