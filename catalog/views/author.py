from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic
from django.urls import reverse_lazy

from catalog.models import Author


class List(generic.ListView):
    # The view passes the context (list of books) by default as
    # object_list and book_list aliases; either will work.

    model = Author
    # customize -> change/filter the query. default: queries all()
    # queryset = Author.objects.all()[:5]
    # Specify your own template name/location. default: modelName_list.html at /app/templates/
    template_name = "catalog/author/list.html"
    # your own name for the list as a template variable. default: modelName_list
    context_object_name = "authors"
    paginate_by = 10

    # Override get_queryset() method to change the list of records returned.
    # This is more flexible than just setting the queryset attribute
    def get_queryset(self):
        return Author.objects.all()[:5]

    # We might also override get_context_data() in order to pass
    # additional context variables to the template (e.g. the list
    # of authors is passed by default)
    def get_context_data(self, **kwargs):
        # When doing this it is important to follow the pattern used above:
        #     First get the existing context from our superclass.
        #     Then add your new context information.
        #     Then return the new (updated) context.

        # Call the base implementation first to get the context
        context = super(List, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['title'] = "Local Library Authors"
        return context


# By default, these views will redirect on success to a page displaying the newly
# created/edited model item, which in our case will be the author detail view we
# created in a previous tutorial. You can specify an alternative redirect location
# by explicitly declaring parameter success_url (as done for the AuthorDelete class)
class Create(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    # The "create" and "update" views use the same template by default, which will
    # be named after your model: *model_name***_form.html** (you can change the
    # suffix to something other than _form using the template_name_suffix field
    # in your view, for example template_name_suffix = '_other_suffix')
    template_name = "catalog/generic_form.html"
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    # You can also specify initial values for each of the fields using a
    # dictionary of field_name/value pairs (here we arbitrarily set the
    # date of death for demonstration purposes — you might want to remove that!)
    initial = {'date_of_death': '11/06/2020'}


class Detail(generic.DetailView):
    model = Author
    template_name = "catalog/author/detail.html"
    queryset = Author.objects.all()


class Update(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    template_name = "catalog/generic_form.html"
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


# The AuthorDelete class doesn't need to display any of the fields, so these don't
# need to be specified. You do however need to specify the success_url, because there
# is no obvious default value for Django to use. In this case, we use the reverse_lazy()
# function to redirect to our author list after an author has been
# deleted — reverse_lazy() is a lazily executed version of reverse(),
# used here because we're providing a URL to a class-based view attribute.
class Delete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.can_mark_returned'

    model = Author
    # The "delete" view expects to find a template named with the format
    # *model_name***_confirm_delete.html** (again, you can change the suffix
    # using template_name_suffix in your view).
    template_name = "catalog/generic_delete.html"
    success_url = reverse_lazy("catalog:author-list")

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        context["type"] = "author"
        return context
