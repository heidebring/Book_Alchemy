from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request

from data.data_models import db
from data.data_manager import (
    add_author_to_db,
    add_book_to_db,
    delete_book_from_db,
    get_all_authors,
    get_all_books,
    get_author_by_name,
    get_book_by_isbn,
    get_book_by_title_and_author,
)
import os

from helper import validate_author_inputs, validate_book_inputs

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)
app.config["TEMPLATE_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

# only once needed
# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    """Route for the list of books where you can search and sort the displayed books"""

    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort", "title")
    order = request.args.get("order", "asc")
    books = get_all_books(search=search, sort_by=sort_by, order=order)
    return render_template("home.html", books=books)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Route for deleting a book with a given id"""

    book = delete_book_from_db(book_id)
    if book is None:
        return "Book not found", 404
    flash("Book successfully deleted", "success")
    return redirect("/")


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Route for adding an author to the application"""

    if request.method == "GET":
        return render_template("add_author.html")

    author_name = request.form.get("name", "")
    birth_date = request.form.get("birth_date", "")
    date_of_death = request.form.get("date_of_death", "")

    validation_errors = validate_author_inputs(author_name, birth_date, date_of_death)
    if len(validation_errors) > 0:
        for error in validation_errors:
            flash(error, "error")
        return render_template("add_author.html")

    author = get_author_by_name(author_name)
    if author:
        flash("Author already exists", "error")
        return render_template("add_author.html")

    try:
        add_author_to_db(author_name, birth_date, date_of_death)
    except Exception as e:
        flash("Something went wrong adding the author", "error")
        app.logger.exception(f"ERROR adding author: {e}")
        return render_template("add_author.html")

    flash("Author added", "success")
    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Route for adding a book to the application"""

    authors = get_all_authors()
    if request.method == "GET":
        return render_template("add_book.html", authors=authors)

    isbn = request.form.get("isbn", "")
    title = request.form.get("title", "")
    author = request.form.get("author", "")
    publication_year = request.form.get("publication_year", "")

    validation_errors = validate_book_inputs(isbn, title, author, publication_year)
    if len(validation_errors) > 0:
        for error in validation_errors:
            flash(error, "error")
        return render_template("add_book.html", authors=authors)

    book_with_isbn = get_book_by_isbn(isbn)
    if book_with_isbn:
        flash("A book with the given isbn already exists", "error")
        return render_template("add_book.html", authors=authors)

    book_with_title_by_author = get_book_by_title_and_author(title, author)
    if book_with_title_by_author:
        flash("A book with the given title already exists for this author", "error")
        return render_template("add_book.html", authors=authors)

    try:
        add_book_to_db(isbn, title, author, publication_year)
    except Exception as e:
        flash("Something went wrong adding the book", "error")
        app.logger.exception(f"ERROR adding book: {e}")
        return render_template("add_book.html", authors=authors)

    flash("Book added", "success")
    return render_template("add_book.html", authors=authors)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
