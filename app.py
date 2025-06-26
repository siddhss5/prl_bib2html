import os
from flask import Flask, render_template
from prl_bib2html import PublicationsConfig, list_publications

app = Flask(__name__)

# PRL-specific configuration
PRL_CONFIG = PublicationsConfig(
    bibtex_base_url=os.environ.get(
        "BIBTEX_BASE_URL", 
        "https://raw.githubusercontent.com/personalrobotics/pubs/refs/heads/siddhss5-href-flip-bug"
    ),
    bibtex_cache_dir=os.environ.get("BIBTEX_CACHE_DIR", "data/bib"),
    pdf_base_dir=os.environ.get("PDF_BASE_DIR", "data/pdf"),
    bib_files=[
        ("siddpubs-journal.bib", "Journal Papers"),
        ("siddpubs-conf.bib", "Conference Papers"),
        ("siddpubs-misc.bib", "Other Papers"),
    ]
)

@app.route("/")
def index():
    return "<h2>Welcome to the PRL Website</h2><p><a href='/publications'>View Publications</a></p>"

@app.route("/publications")
def publications():
    pubs = list_publications(PRL_CONFIG)
    return render_template("publications.html", pubs=pubs)

if __name__ == "__main__":
    app.run(debug=True)