from flask import Flask, render_template
from publications import list_publications

app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>Welcome to the PRL Website</h2><p><a href='/publications'>View Publications</a></p>"

@app.route("/publications")
def publications():
    pubs = list_publications()
    return render_template("publications.html", pubs=pubs)

if __name__ == "__main__":
    app.run(debug=True)