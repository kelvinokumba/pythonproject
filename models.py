#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLite database engine
engine = create_engine('sqlite:///book_library.db')
# Create a base class for declarative models
Base = declarative_base()

# Define a many-to-many association table between books and genres
book_genre = Table(
    'book_genres',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id')),
    extend_existing=True,
)

class Book(Base):
    """
    Represents a book in the library.
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    publication_date = Column(Date)
    isbn = Column(String, unique=True)

    # Define a relationship with Author
    author = relationship("Author", back_populates="books", foreign_keys=[author_id])

    # Define a many-to-many relationship with Genre through the book_genre association table
    genres = relationship("Genre", secondary=book_genre, back_populates="books")

    def __repr__(self):
        return f"Title: {self.title}, was published on {self.publication_date}"

class Author(Base):
    """
    Represents an author of a book.
    """
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bio = Column(String)

    # Define a one-to-many relationship with Book
    books = relationship('Book', back_populates='author', foreign_keys=[Book.author_id])

    def __repr__(self):
        return f"Written by: {self.name}, description: {self.bio}"

class Genre(Base):
    """
    Represents a genre of books.
    """
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Define a many-to-many relationship with Book through the book_genre association table
    books = relationship("Book", secondary=book_genre, back_populates="genres")

    def __repr__(self):
        return f"Genre: {self.name}, has an id of {self.id}"

class UserProfile(Base):
    """
    Represents user profiles for authentication.
    """
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"username: {self.username}"

if __name__ == "__main__":
    # Create a SQLite database engine
    engine = create_engine('sqlite:///book_library.db')

    # Create database tables based on defined models
    # Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
