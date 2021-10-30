from django.db import models

from .author import Author
from .base import BaseModel
from .genre import Genre


# Warning: By default on_delete=models.CASCADE, which means that if the
# author was deleted, this book would be deleted too! We use SET_NULL
# here, but we could also use PROTECT or RESTRICT to prevent the author
# being deleted while any book uses it.


class Book(BaseModel):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=255)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # null=True, which allows the database to store a Null value if no author is selected
    # on_delete=models.SET_NULL, which will set the value of the book's
    # author field to Null if the associated author record is delete
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000,
                               help_text='Enter a brief description of the book')
    isbn = models.CharField("ISBN", max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    @property
    def detail_url(self) -> str:
        return "catalog:book-detail"

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"
