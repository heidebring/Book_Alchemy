from datetime import date
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class Author(db.Model):
    """Represents an author with attributes id, name, birth_date and date_of_death"""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    birth_date: Mapped[date]
    date_of_death: Mapped[Optional[date]]


class Book(db.Model):
    """Represents a book with attributes id, isbn, title, author and publication_year"""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str]
    title: Mapped[str]
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    publication_year: Mapped[int]
