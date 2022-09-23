'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_all_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')

    def test_wrong_input_type_to_years(self):
        self.assertRaises(TypeError, self.books_between_years, 1920, [1940])
        self.assertRaises(TypeError, self.books_between_years, [], [])
        self.assertRaises(TypeError, self.books_between_years, "bom dia", 1940)
        self.assertRaises(TypeError, self.books_between_years, "asd", [])

    def test_all_books_years(self):
        self.assertEqual(len(self.books_between_years), len(self.data_source))

    def test_no_books_years(self):
        self.assertEqual(len(self.books_between_years(100000, 100001), 0))

    def test_inverted_range_years(self):
        self.assertEqual(len(self.books_between_years(1000000, 0), 0))

    def test_sorted_by_year(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books_beween_years()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Omoo')
        self.assertTrue(books[2].title == 'Neverwhere')

    def test_sorted_tied_years(self):
        books = self.books_between_years(1982, 1987)
        assertEqual(books[0].title, 'A Wild Sheep Chase')
        assertEqual(books[1].title, 'Hard-Boiled Wonderland and the End of the World')
        assertEqual(books[2].title, 'Love in the Time of Cholera')
        assertEqual(books[3].title, 'Shards of Honor')
        assertEqual(books[4].title, 'Beloved')

    def test_years_no_ending(self):
        assertEqual(self.books_between_years(1995), self.books_between_years(1995, 100000))

    def test_years_no_beginning(self):
        assertEqual(self.books_between_years(None, 1990), self.books_between_years(-100000, 1990))
    
if __name__ == '__main__':
    unittest.main()

