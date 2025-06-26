import os
from flask import Flask, render_template, redirect, url_for
from prl_bib2html import PublicationsConfig, list_publications

app = Flask(__name__, template_folder='templates')

# PRL-specific configuration
PRL_CONFIG = PublicationsConfig(
    bibtex_base_url=os.environ.get(
        "BIBTEX_BASE_URL", 
        "https://raw.githubusercontent.com/personalrobotics/pubs/refs/heads/siddhss5-href-flip-bug"
    ),
    bibtex_cache_dir=os.environ.get("BIBTEX_CACHE_DIR", "data/bib"),
    pdf_base_dir=os.environ.get("PDF_BASE_DIR", "https://personalrobotics.cs.washington.edu/publications/"),
    bib_files=[
        ("siddpubs-journal.bib", "Journal Papers"),
        ("siddpubs-conf.bib", "Conference Papers"),
        ("siddpubs-misc.bib", "Other Papers"),
    ]
)

@app.route("/")
def index():
    return redirect(url_for('publications'))

@app.route("/publications")
def publications():
    pubs = list_publications(PRL_CONFIG)
    return render_template("publications.html", pubs=pubs)

if __name__ == "__main__":
    app.run(debug=True)