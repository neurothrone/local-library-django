import datetime

from django.test import SimpleTestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


# Here we don't actually use the database or test client.
# Consider modifying these tests to use SimpleTestCase.
class RenewBookFormTest(SimpleTestCase):
    # SimpleTestCase and its subclasses (e.g. TestCase, …) rely on setUpClass()
    # and tearDownClass() to perform some class-wide initialization (e.g. overriding
    # settings). If you need to override those methods, don’t forget to call the
    # super implementation:

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ...

    @classmethod
    def tearDownClass(cls):
        ...
        super().tearDownClass()

    # Note here that we also have to test whether the label value is None,
    # because even though Django will render the correct label it returns
    # None if the value is not explicitly set.
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
