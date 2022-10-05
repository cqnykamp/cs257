#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.

    Modified by Luca Araújo and Charles Nykamp, 05 October 2022

'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.books_list = []

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

def get_given_name(string):
    return string.split(' ')[0]

def get_surname(string):
    working_string = string.split(' ')
    surname = ''
    for i in range(1, len(working_string)):
        substring = working_string[i]
        if substring[0] == '(':
            break
        if surname != '':
            surname += ' '
        surname += substring
    return surname

def get_birth(string):
    value = string.split(' ')[-1].split('-')[0][1:]
    if value == '':
        return None
    return (int)(value)

def get_death(string):
    value = string.split(' ')[-1].split('-')[1][:-1]
    if value == '':
        return None
    return (int)(value)


class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.authors_list = []
        self.books_list = []
        with open(books_csv_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                authors_unprocessed_list = row[2].split(' and ')
                authors_list_local = []

                for author in authors_unprocessed_list:
                    new_author = Author(get_surname(author), get_given_name(author), get_birth(author), get_death(author))
                    authors_list_local.append(new_author)

                new_book = Book(row[0], (int)(row[1]), authors_list_local)
                self.books_list.append(new_book)

                for author in authors_list_local:
                    if author not in self.authors_list:
                        author.books_list.append(new_book)
                        self.authors_list.append(author)
                    else:
                        self.authors_list[self.authors_list.index(author)].books_list.append(new_book)

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        ans = []
        if search_text == None:
            ans = self.authors_list
        else:
            for i in range(len(self.authors_list)):
                if search_text.lower() in (self.authors_list[i].given_name + ' ' + self.authors_list[i].surname).lower():
                    ans.append(self.authors_list[i])

        ans.sort(key=lambda author: (author.surname.lower(), author.given_name.lower()))

        return ans

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        ans = []
        if search_text == None:
            ans = self.books_list
        else:
            for i in range(len(self.books_list)):
                if search_text.lower() in self.books_list[i].title.lower():
                    ans.append(self.books_list[i])

        if sort_by.lower() == 'year':
            ans.sort(key=lambda book: (book.publication_year, book.title.lower()))
        else: 
            ans.sort(key=lambda book: (book.title.lower(), book.publication_year))

        return ans

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        if start_year == None:
            start_year = -1000000
        if end_year == None:
            end_year = 1000000

        ans = []
        for i in range(len(self.books_list)):
            if self.books_list[i].publication_year >= start_year and self.books_list[i].publication_year <= end_year:
                ans.append(self.books_list[i])

        ans.sort(key=lambda book: (book.publication_year, book.title.lower()))

        return ans

