from django.urls import path
from django.urls import re_path

from catalog import views
from catalog.views import author
from catalog.views import book

app_name = "catalog"
urlpatterns = [
    # Warning: The generic class-based detail view expects to be passed a parameter
    # named pk. If you're writing your own function view you can use whatever parameter
    # name you like, or indeed pass the information in an unnamed argument.

    path("", views.IndexView.as_view(), name="index"),

    path("authors/", author.List.as_view(), name="author-list"),
    path("author/<int:pk>/", author.Detail.as_view(), name="author-detail"),
    path("author/create/", author.Create.as_view(), name="author-create"),
    path("author/<int:pk>/update/", author.Update.as_view(), name="author-update"),
    path("author/<int:pk>/delete/", author.Delete.as_view(), name="author-delete"),

    path("books/", book.List.as_view(), name="book-list"),
    path("book/<int:pk>/", book.Detail.as_view(), name="book-detail"),
    path("book/create/", book.Create.as_view(), name="book-create"),
    path("book/<int:pk>/update/", book.Update.as_view(), name="book-update"),
    path("book/<int:pk>/delete/", book.Delete.as_view(), name="book-delete"),

    # re_path(r'^book/(?P<pk>\d+)$', book.Detail.as_view(), name='book-detail'),
    # re_path(r"^books/(?P<dt>\d{4}}[-]\d{2}[-]\d{2})$"),

    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="book-borrowed"),
    path("borrowed/", views.LibrarianListView.as_view(), name="book-librarian-borrowed"),
    path("book/<uuid:pk>/renew/", views.LibrarianRenewBook.as_view(), name="book-librarian-renew"),
]
