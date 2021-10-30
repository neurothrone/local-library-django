from django.db import models


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(max_length=200,
                            help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)')

    def __str__(self) -> str:
        """String for representing the Model object."""
        return self.name
