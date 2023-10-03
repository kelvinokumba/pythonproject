import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Author, Book, Genre, Base

if __name__ == "__main__":
    # Create a SQLite database engine
    engine = create_engine('sqlite:///book_library.db')

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a Faker instance for generating random data
    fake = Faker()

    # List of genres
    genre_list = [
        'Mystery',
        'Science Fiction',
        'Fantasy',
        'Romance',
        'Thriller',
        'Non-Fiction',
        'Historical Fiction',
        'Biography',
        'Self-Help',
        'Cooking'
    ]

    # Create and add Genre instances
    genres = []
    for genre_name in genre_list:
        genre = Genre(name=genre_name)
        genres.append(genre)
        session.add(genre)

    session.commit()

    # Create and add Author instances
    authors = []
    for _ in range(10):
        author = Author(
            name=fake.name(),
            bio=fake.text()
        )
        authors.append(author)
        session.add(author)

    session.commit()

    # Create and add Book instances with relationships
    books = []
    for _ in range(20):  # You can adjust the number of books as needed
        author = random.choice(authors)
        genre = random.choice(genres)
        book = Book(
            title=fake.catch_phrase(),
            author=author,
            genre_id=genre.id,  # Use genre_id to specify the genre
            publication_date=fake.date_of_birth(minimum_age=18, maximum_age=100),
            isbn=fake.isbn13()
        )

        books.append(book)
        session.add(book)

    session.commit()
