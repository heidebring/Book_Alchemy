from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

from data_models import (
    add_author_to_db,
    add_book_to_db,
    db,
    Author,
    Book,
    get_all_authors,
)
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)
app.config["TEMPLATE_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)

db.init_app(app)

# only once needed
with app.app_context():
    db.create_all()


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "GET":
        return render_template("add_author.html")

    author_name = request.form.get("name", "")
    birth_date = request.form.get("birth_date", "")
    date_of_death = request.form.get("date_of_death", "")

    try:
        add_author_to_db(author_name, birth_date, date_of_death)
    except Exception as e:
        app.logger.exception(f"ERROR adding author: {e}")
        return render_template("add_author.html")

    return render_template(
        "add_author.html", success_message=f"Author {author_name} added"
    )


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    authors = get_all_authors()
    if request.method == "GET":
        return render_template("add_book.html", authors=authors)

    isbn = request.form.get("isbn", "")
    title = request.form.get("title", "")
    author = request.form.get("author", "")
    publication_year = request.form.get("publication_year", "")

    try:
        add_book_to_db(isbn, title, author, publication_year)
    except Exception as e:
        app.logger.exception(f"ERROR adding book: {e}")
        return render_template("add_book.html")

    return render_template(
        "add_book.html", authors=authors, success_message=f"Book {title} added"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
