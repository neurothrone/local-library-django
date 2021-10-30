from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog:author-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('catalog:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author/list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('catalog:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('catalog:author-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 3)

# The most interesting variable we demonstrate above is response.context, which is the
# context variable passed to the template by the view. This is incredibly useful for
# testing, because it allows us to confirm that our template is getting all the data
# it needs. In other words we can check that we're using the intended template and
# what data the template is getting, which goes a long way to verifying that any
# rendering issues are solely due to template.
