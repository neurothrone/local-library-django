from django.db import models

from .base import BaseModel


class Author(BaseModel):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def detail_url(self) -> str:
        return "catalog:author-detail"

    def __str__(self) -> str:
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
