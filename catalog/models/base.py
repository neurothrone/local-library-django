from abc import abstractmethod

from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @property
    @abstractmethod
    def detail_url(self) -> str:
        raise NotImplementedError()

    def get_absolute_url(self):
        """Returns the url to access a detail record for this object."""
        return reverse(self.detail_url, args=[str(self.id)])
