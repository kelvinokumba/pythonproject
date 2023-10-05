#!/usr/bin/env python3

import click
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker
from models import Book, Author, Genre, engine

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

class BookLibraryCLI:
    def add_book(self, title, author_id, genre_id, publication_date, isbn):
        """
        Add a new book to the library database.

        Args:
            title (str): The title of the book.
            author_id (int): The ID of the author.
            genre_id (int): The ID of the genre.
            publication_date (str): The publication date in 'YYYY-MM-DD' format.
            isbn (str): The ISBN of the book.

        Returns:
            None
        """
        book = Book(
            title=title,
            author_id=author_id,
            genre_id=genre_id,
            publication_date=publication_date,
            isbn=isbn,
        )
        session.add(book)
        session.commit()

    def search_books(self, author=None, genre=None):
        """
        Search for books in the library database based on author or genre.

        Args:
            author (str): The name of the author to search for.
            genre (str): The genre to search for.

        Returns:
            list: A list of books that match the search criteria.
        """
        query = session.query(Book)
        if author:
            query = query.filter(Book.author_name == author)
        elif genre:
            query = query.filter(Book.genre_name == genre)

        books = query.all()
        return books

    def get_books(self, author=None, genre=None):
        """
        Get a list of books from the library database based on author or genre.

        Args:
            author (str): The name of the author to filter by.
            genre (str): The genre to filter by.

        Returns:
            list: A list of books that match the filter criteria.
        """
        query = session.query(Book)

        if author:
            query = query.filter(Book.author.has(name=author))
        elif genre:
            query = query.filter(Book.genres.any(name=genre))

        books = query.all()
        return books

    def format_book_list(self, books):
        """
        Format a list of books into a user-friendly format.

        Args:
            books (list): A list of Book objects.

        Returns:
            list: A list of dictionaries representing formatted book information.
        """
        formatted_books = []
        for book in books:
            formatted_book = {
                'Title': book.title,
                'Author': book.author.name,
                'Genre': ', '.join([genre.name for genre in book.genres]),
                'Publication Date': str(book.publication_date),
                'ISBN': book.isbn
            }
            formatted_books.append(formatted_book)
        return formatted_books
    
    def delete_book(self, book_id):
        """
        Delete a book from the library database.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if the book was successfully deleted, False otherwise.
        """
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return True
        return False

# Define CLI commands
@click.command()
@click.option('--title', prompt='Title')
@click.option('--author_id', prompt='Author ID')
@click.option('--genre_id', prompt='Genre ID')
@click.option('--publication_date', prompt='Publication Date (YYYY-MM-DD)')
@click.option('--isbn', prompt='ISBN')
def add_book_command(title, author_id, genre_id, publication_date, isbn):
    # Parse the publication_date string into a Python date object
    try:
        publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
    except ValueError:
        click.echo("Invalid date format. Please use YYYY-MM-DD format.")
        return

    cli = BookLibraryCLI()
    cli.add_book(title, author_id, genre_id, publication_date, isbn)
    click.echo("Book added successfully.")

@click.command()
@click.option('--book_id', prompt='Book ID to delete', type=int)
def delete_book_command(book_id):
    cli = BookLibraryCLI()
    if cli.delete_book(book_id):
        click.echo("Book deleted successfully.")
    else:
        click.echo("Book not found with the provided ID.")

# Extend the search_command function to allow interaction
@click.command()
@click.option('--author', help='Search books by author')
@click.option('--genre', help='Search books by genre')
@click.option('--author_id', help='Search books by author ID', type=int)
def search_command(author, genre, author_id):
    cli = BookLibraryCLI()

    if author_id is not None:
        books = cli.search_books(book_id=author_id)
    else:
        books = cli.get_books(author=author, genre=genre)

    if not books:
        click.echo("No books found.")
    else:
        formatted_books = cli.format_book_list(books)
        click.echo("Books found:")
        for index, book in enumerate(formatted_books, start=1):
            click.echo(f"{index}. {book['Title']} by {book['Author']}")
        
        while True:
            choice = click.prompt(
                "Select a book to interact with (enter the number) or 'q' to quit: ",
                type=str
            )

            if choice == 'q':
                break
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(formatted_books):
                    selected_book = formatted_books[index]
                    click.echo(f"Selected Book: {selected_book['Title']} by {selected_book['Author']}")
                    # Here, you can provide options for further interaction with the selected book
                else:
                    click.echo("Invalid book number. Please select a valid number.")
            else:
                click.echo("Invalid input. Enter a number or 'q' to quit.")

# Define the welcome_message command
@click.command()
def welcome_message():
    click.echo("Welcome to the Book Library CLI!")
    while True:
        choice = click.prompt(
            "Choose an option:\n1. Add a book\n2. Search for a book\n3. Delete a book\n4. Quit\n", type=int
        )
        
        if choice == 1:
            add_book_command()
        elif choice == 2:
            search_command()
        elif choice == 3:
            delete_book_command()
        elif choice == 4:
            click.echo("Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please select 1, 2, 3, or 4.")

# Main program execution
if __name__ == '__main__':
    welcome_message()
