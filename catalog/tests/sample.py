from django.test import TestCase


class YourTestClassExample(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)


# Note: The test classes also have a tearDown() method which we haven't used. This method
# isn't particularly useful for database tests, since the TestCase base class takes care of
# database teardown for you.
class YourTestClassExample2(TestCase):
    # The AssertTrue, AssertFalse, AssertEqual are standard assertions provided by unittest.
    # There are other standard assertions in the framework, and also Django-specific assertions
    # to test if a view redirects (assertRedirects), to test if a particular template has been
    # used (assertTemplateUsed), etc.

    # setUpTestData() is called once at the beginning of the test run for class-level setup.
    # You'd use this to create objects that aren't going to be modified or changed in any of
    # the test methods.
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    # setUp() is called before every test function to set up any objects that may be modified
    # by the test (every test function will get a "fresh" version of these objects).
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
