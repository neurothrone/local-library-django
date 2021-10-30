import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views import generic

from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm
from catalog.models import Book
from catalog.models import BookInstance
from catalog.models import Author
from catalog.models import Genre


class IndexView(View):
    """View function for home page of site."""

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        # Number of visits to this view, as counted in the session variable.
        num_visits = request.session.get("num_visits", 0)
        request.session["num_visits"] = num_visits + 1

        context = {
            "num_visits": num_visits,
            # Generate counts of some of the main objects
            "num_books": Book.objects.all().count(),
            "num_instances": BookInstance.objects.all().count(),
            # Available books (status = 'a')
            "num_instances_available": BookInstance.objects.filter(status__exact="a").count(),
            "num_authors": Author.objects.count(),  # The 'all()' is implied by default.
            "num_genres": Genre.objects.count(),
            "num_books_dune": Book.objects.filter(title__icontains="dune").count(),
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, "catalog/index.html", context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    # You can also specify an alternative location to redirect the user to if
    # they are not authenticated (login_url), and a URL parameter name instead
    # of "next" to insert the current absolute path (redirect_field_name).
    # login_url = "/accounts/login/"
    # redirect_field_name = "/catalog/mybooks/"

    model = BookInstance
    template_name = "catalog/book/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user) \
            .filter(status__exact="o").order_by("due_back")


class LibrarianListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    # permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
    model = BookInstance
    context_object_name = "books"
    template_name = "catalog/book/librarian_view_borrowed_books.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


class LibrarianRenewBook(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Class-based view for renewing a specific BookInstance by librarian."""

    permission_required = 'catalog.can_mark_returned'

    @staticmethod
    def get(request: HttpRequest, pk: str) -> HttpResponse:
        book_instance = get_object_or_404(BookInstance, pk=pk)
        proposed_renewal_data = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_data})
        context = {
            "form": form,
            "book_instance": book_instance,
        }
        return render(request, "catalog/book/librarian_renew_book.html", context)

    @staticmethod
    def post(request: HttpRequest, pk: str) -> HttpResponse:
        book_instance = get_object_or_404(BookInstance, pk=pk)

        # Create a form instance and populate it with data from the request (binding)
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("catalog:book-librarian-borrowed"))

        context = {
            "form": form,
            "book_instance": book_instance,
        }
        return render(request, "catalog/book/librarian_renew_book.html", context)
