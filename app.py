from flask import Flask, redirect, render_template, request


from data_models import (
    add_author_to_db,
    add_book_to_db,
    db,
    delete_book_from_db,
    get_all_authors,
    get_all_books,
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
success_message = ""

# only once needed
# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    """Route for the list of books where you can search and sort the displayed books"""

    global success_message
    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort", "title")
    order = request.args.get("order", "asc")
    books = get_all_books(search=search, sort_by=sort_by, order=order)
    return render_template("home.html", books=books, success_message=success_message)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Route for deleting a book with a given id"""

    global success_message
    book = delete_book_from_db(book_id)
    if book is None:
        return "Book not found", 404
    success_message = "Book successfully deleted"
    return redirect("/")


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Route for adding an author to the application"""

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
    """Route for adding a book to the application"""

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
