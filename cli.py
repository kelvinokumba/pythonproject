import click
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker
from models import Book, Author, Genre, engine

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

class BookLibraryCLI:
    def add_book(self, title, author_id, genre_id, publication_date, isbn):
        book = Book(
            title=title,
            author_id=author_id,
            genre_id=genre_id,
            publication_date=publication_date,
            isbn=isbn,
        )
        session.add(book)
        session.commit()

    def search_books(self, author=None, genre=None, book_id=None):
        query = session.query(Book)
        if author:
            query = query.filter(Book.author_name == author)
        elif genre:
            query = query.filter(Book.genre_name == genre)
        elif book_id is not None:
            query = query.filter(Book.id == book_id)

        books = query.all()
        return books

    def get_books(self, author=None, genre=None):
        query = session.query(Book)

        if author:
            query = query.filter(Book.author.has(name=author))
        elif genre:
            query = query.filter(Book.genres.any(name=genre))

        books = query.all()
        return books

    def format_book_list(self, books):
        formatted_books = []
        for book in books:
            formatted_book = {
                'ID': book.id,
                'Title': book.title,
                'Author': book.author.name,
                'Genre': ', '.join([genre.name for genre in book.genres]),
                'Publication Date': str(book.publication_date),
                'ISBN': book.isbn
            }
            formatted_books.append(formatted_book)
        return formatted_books

@click.command()
@click.option('--title', prompt='Title')
@click.option('--author_id', prompt='Author ID')
@click.option('--genre_id', prompt='Genre ID')
@click.option('--publication_date', prompt='Publication Date (YYYY-MM-DD)')
@click.option('--isbn', prompt='ISBN')
def add_book_command(title, author_id, genre_id, publication_date, isbn):
   
    try:
        publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
    except ValueError:
        click.echo("Invalid date format. Please use YYYY-MM-DD format.")
        return

    cli = BookLibraryCLI()
    cli.add_book(title, author_id, genre_id, publication_date, isbn)
    click.echo("Book added successfully.")

@click.command()
@click.option('--author', help='Search books by author')
@click.option('--genre', help='Search books by genre')
@click.option('--book_id', help='Search book by ID', type=int)
def search_command(author, genre, book_id):
    cli = BookLibraryCLI()
    if book_id is not None:
        books = cli.search_books(book_id=book_id)
    else:
        books = cli.get_books(author, genre)

    if not books:
        click.echo("No books found.")
    else:
        formatted_books = cli.format_book_list(books)
        click.echo("Books found:")
        for book in formatted_books:
            for key, value in book.items():
                click.echo(f"{key}: {value}")
            click.echo("\n")

@click.command()
def welcome_message():
    click.echo("Welcome to the Book Library CLI!")
    choice = click.prompt("Choose an option:\n1. Add a book\n2. Search for a book\n", type=int)
    
    if choice == 1:
        add_book_command()
    elif choice == 2:
        book_id = click.prompt("Enter the Book ID to search", type=str)
        search_command(book_id=book_id)
    else:
        click.echo("Invalid choice. Please select 1 or 2.")

if __name__ == '__main__':
    welcome_message()
