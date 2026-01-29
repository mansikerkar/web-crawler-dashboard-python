from flask import Flask, render_template, request
from crawler import crawl
from db import init_db, insert_pages, fetch_pages

app = Flask(__name__)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        depth = int(request.form["depth"])
        keyword = request.form.get("keyword")

        pages = crawl(url, depth, keyword)
        insert_pages(pages)

        return render_template("results.html", pages=pages)

    return render_template("index.html")

@app.route("/stored")
def stored():
    pages = fetch_pages()
    return render_template("results.html", pages=pages)

if __name__ == "__main__":
    app.run(debug=True)
