from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Book


class List(generic.ListView):
    model = Book
    template_name = "catalog/book/list.html"
    context_object_name = "books"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        context["title"] = "Book List"
        return context


class Create(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    template_name = "catalog/generic_form.html"
    fields = ['title', 'author', 'summary', 'isbn', "genre", "language"]


# If a requested record does not exist then the generic class-based detail
# view will raise an Http404 exception for you automatically — in production,
# this will automatically display an appropriate "resource not found" page,
# which you can customise if desired.
class Detail(generic.DetailView):
    model = Book
    template_name = "catalog/book/detail.html"
    context_object_name = "book"


class Update(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    template_name = "catalog/generic_form.html"
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class Delete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.can_mark_returned'

    model = Book
    template_name = "catalog/generic_delete.html"
    success_url = reverse_lazy("catalog:book-list")

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        context["type"] = "book"
        return context
