'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021

   Modified by Luca Araújo and Charles Nykamp, 23 September 2022

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

    def test_author_case_insensitive(self):
        authors = self.data_source.authors('lEWiS')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Lewis', 'Sinclair'))

    def test_all_authors(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors()
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Austen', 'Jane'))
        self.assertTrue(authors[1] == Author('Gaiman', 'Neil'))
        self.assertTrue(authors[2] == Author('Melville', 'Herman'))
    
    def test_nonexistent_author(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors('asdfasdfasdf')
        self.assertTrue(len(authors) == 0)
    
    def test_author_same_surname(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))
        self.assertTrue(authors[1] == Author('Brontë', 'Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë', 'Emily'))
    
    def test_author_search_only_given_name(self):
        authors = self.data_source.authors('peg')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Orenstein', 'Peggy'))

    def test_author_two_word_surname(self):
        authors = self.data_source.authors('garc')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('García Márquez', 'Gabriel'))

    def test_author_abbreviated_given_name(self):
        authors = self.data_source.authors('V.')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Schwab', 'V.E.'))

    def test_author_search_full_name(self):
        authors = self.data_source.authors('Haruki Murakami')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Murakami', 'Haruki'))


    def test_books_normal_keyword(self):
        books = self.data_source.books('love')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book("Beloved"))
        self.assertTrue(books[1] == Book("Love in the Time of Cholera"))

    def test_books_with_comma(self):
        books = self.data_source.books('fine')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book("Fine, Thanks"))

    def test_books_sort_by_year(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books('M', 'year')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book("Emma"))
        self.assertTrue(books[1] == Book("Omma"))

    def test_books_sort_by_title(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books('M', 'title')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book("Emma"))
        self.assertTrue(books[1] == Book("Omma"))

    def test_books_nonexistent_keyword(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books('qwerty no book has this title')
        self.assertTrue(len(books) == 0)


    


    

if __name__ == '__main__':
    unittest.main()

