from datetime import date
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    birth_date: Mapped[date]
    date_of_death: Mapped[Optional[date]]


class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str]
    title: Mapped[str]
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    publication_year: Mapped[int]


def add_author_to_db(author_name, birth_date, date_of_death):
    birth_date = date.fromisoformat(birth_date)
    if not date_of_death:
        date_of_death = None
    else:
        date_of_death = date.fromisoformat(date_of_death)
    try:
        author = Author(
            name=author_name,
            birth_date=birth_date,
            date_of_death=date_of_death,
        )
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def get_all_authors():
    return Author.query.order_by(
        Author.name,
    ).all()


def add_book_to_db(isbn, title, author, publication_year):
    try:
        book = Book(
            isbn=isbn, title=title, author=author, publication_year=publication_year
        )
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
