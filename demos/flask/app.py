"""
Flask web application demo for labdata.

Shows how to use labdata in a Flask web application
to display publications, people, and projects.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import os
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from labdata import LabDataConfig, assemble

app = Flask(__name__, template_folder='templates')

# Load configuration and assemble data at startup
CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.yaml")
CONFIG_PATH = Path(__file__).parent / CONFIG_FILE

config = LabDataConfig.from_yaml(str(CONFIG_PATH))
DATA = assemble(config)


@app.route("/")
def index():
    return redirect(url_for('publications'))


@app.route("/publications")
def publications():
    return render_template("publications.html", publications=DATA.publications)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=DATA.projects)


@app.route("/people")
def people():
    return render_template("people.html", people=DATA.people)


if __name__ == "__main__":
    app.run(debug=True)
