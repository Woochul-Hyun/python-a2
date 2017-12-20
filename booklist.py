from book import Book
from operator import attrgetter


class BookList:

    def __init__(self):
        """
        Initializes a BookList
        """
        self.booklists = []

    def get_book_by_title(self, title=''):
        """
        This method take title of book
        :return: Book object with that title
        """
        for book in self.booklists:
            if book.title == title:
                return book

    def add_book(self, book = Book()):
        """
        This method appends a book to the booklists
        :param book: book is an instance of the Class "Book"
        :return: None
        """
        self.booklists.append(book)

    def get_total_pages(self, status):
        """
        This method takes total pages of required book and completed book
        :param status: "r" or "c"
        :return: total number of pages of completed book and required book
        """
        pages = 0                           # set the initial number of page to 0
        for book in self.booklists:
            if book.status == status:
                pages += int(book.pages)    # add the number of page to total pages
        return pages


    def load_file(self):
        """
        This method load files(books) from "book.csv"
        :return: loaded book
        """
        my_file = open("books.csv", 'r')                        # open "books.csv" and read the content
        for index, new_list in enumerate(my_file.readlines()):
            new_data = new_list.strip().split(',')              # using the '.split' method to split each line in the file by the comma
            book = Book(new_data[0], new_data[1], int(new_data[2]), new_data[3])
            self.booklists.append(book)
        self.sort_books()
        my_file.close()

    def save_file(self):
        """
        This method save book from booklist (required book and completed book) to "book.csv" file
        :return: None
        """
        self.sort_books()
        output_file = open("books.csv", 'w')
        for book in self.booklists:
            output_file.write('{},{},{},{}\n'.format(book.title, book.author, book.pages, book.status))
        output_file.close()

    def sort_books(self):
        """
        This method sort the book in booklist by author name first then sort by number of pages
        """
        self.booklists.sort(key=attrgetter('author', 'pages'))

