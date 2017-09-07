# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
# NOTE: It cannot be run with pytest.

import unittest
import parametrized_test_case
import importlib

import directory
import wikiquotes
import file_manager
import Author

random_tries = 3

class AuthorTest(parametrized_test_case.ParametrizedTestCase):

    def test_get_quotes(self):
        language = importlib.import_module(self.author.language)
        fetch_quotes = wikiquotes.get_quotes(self.author.name, language)

        self.assertTrue(set(self.author.quotes).issubset(set(fetch_quotes)))

    def test_quotes_length(self):
        language = importlib.import_module(self.author.language)
        fetch_quotes = wikiquotes.get_quotes(self.author.name, language)
        # It is probable that new quotes are added.
        # The assumption is that quotes aren't removed.
        # So quotes fetched must be at least the number seen.
        # We don't want tests to break if there is a new quote.
        self.assertTrue(len(fetch_quotes) >= len(self.author.quotes))

        # No repeated elements
        self.assertEqual(len(fetch_quotes), len(set(fetch_quotes)))

    def test_random_quote(self):
        language = importlib.import_module(self.author.language)
        fetch_quotes = wikiquotes.get_quotes(self.author.name, language)
        number_of_quotes = len(fetch_quotes)

        if number_of_quotes == 1:
            return

        if number_of_quotes > 1:
            for i in range(0, random_tries):
                random_quote = wikiquotes.random_quote(self.author.name, language)
                other_random_quote = wikiquotes.random_quote(self.author.name, language)

                if not random_quote == other_random_quote:
                    return

        self.fail("Incorrect random quotes for {}".format('Reuben_Abel'))

    @property
    def author(self):
        return self.parameter

def main():
    suite = unittest.TestSuite()
    tests = map(_create_test_for_author, _fetch_all_authors())

    for test in tests:
        suite.addTest(test)

    unittest.TextTestRunner(verbosity=2).run(suite)

def _fetch_all_authors():
    return file_manager.list_absolute_files_with_extension(directory.authors_directory, ".txt")

def _create_test_for_author(author_test_file_path):
    author = Author.Author(author_test_file_path)
    return parametrized_test_case.ParametrizedTestCase.parametrize(AuthorTest, parameter=author)

if __name__ == '__main__':
    main()
