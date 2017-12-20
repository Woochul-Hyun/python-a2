"""
Name: Woochul Hyun
Student ID: 13377156
Date: 29 / 09 / 2017

Brief Project Description:This program uses Kivy to display the reading list to the user through the GUI.
The user can change the required book to completion and add a new book.
Through the program, you can check the required book, completed book and check the number of pages.
When you add a new book, you need to enter a title, artist, and page.
These added books are automatically saved in the CSV file at the end of the program.

GitHub URL: https://github.com/CP1404-JCUS/a2-reading-list-Woochul-Hyun
"""

from kivy.app import App                        # importing App from kivy.app library
from kivy.lang import Builder                   # importing Builder from kivy.lang library
from kivy.uix.button import Button              # importing Button from kivy.uix.button library
from kivy.properties import StringProperty      # importing StringProperty from kivy.properties library
from book import Book                           # importing Book from the book.py
from booklist import BookList                   # importing BookList from the booklist.py
from kivy.core.window import Window             # importing Window from the kivy.core.window library
import string                                   # importing string module to check the error

FILE_NAME = "books.csv"
over_500_pages_book_colour = (0, 1, 1, 1)       # set the colour for long book which has 500 pages or more
under_500_pages_book_colour = (0, 1, 0, 1)      # set the colour for long book which has under 500 pages
complited_book_colour = (0.5, 0.5, 0.5, 1)      # set the colour for completed book

class ReadingListApp(App):
    """
    This is main class for this entire programm
    """

    top_label = StringProperty()
    bottom_label = StringProperty()

    def on_start(self):                 # initializing the program
        print("Programm is called.")
        self.book_button("r")

    def build(self):
        """
        set Kivy for GUI
        :return: root kivy widget
        """
        self.status_text = "Reading List App 2.0"
        self.title = "Reading list 2.0"
        self.root = Builder.load_file("app.kv")
        Window.size = (1000, 650)       # window size
        return self.root

    def __init__(self, **kwargs):
        """
        main application build
        """
        super().__init__(**kwargs)
        self.list_books = BookList()
        self.list_books.load_file()

    def display_book_list(self, required_or_complited):
        """
        This function create button for required book and completed book and put th book in to the interface to display
        Also, display the book with different colour depend on the number of pages
        :param required_or_complited: "True" is required book and "False" is completed book
        :return: None
        """
        self.root.ids.displayBookList.clear_widgets()

        if required_or_complited == True:
            for book in self.list_books.booklists:
                if book.status == 'r':
                    button = Button(text=book.title)
                    button.bind(on_release=self.required_book)
                    if book.longBook():                                         # check ths number of pages of book whether the page is over 500
                        button.background_color = over_500_pages_book_colour    # put the colour which is set on the first part of programm for over 500 pages Book
                    else:
                        button.background_color = under_500_pages_book_colour   # put the colour which is set on the first part of programm for under 500 pages Book
                    self.root.ids.displayBookList.add_widget(button)
            self.bottom_label = "Click books to mark them as completed"         #display the message on botton bar
            self.top_label = "Total pages to read: {}".format(self.list_books.get_total_pages("r"))

        elif required_or_complited == False:
            for book in self.list_books.booklists:
                if book.status == 'c':
                    button = Button(text=book.title)
                    button.bind(on_release=self.completed_book)
                    button.background_color = complited_book_colour             # put the colour which is set on the first part of programm for completed book
                    self.root.ids.displayBookList.add_widget(button)
            self.bottom_label = 'Click the book to see the details'             #display the message on botton bar
            self.top_label = "Total pages completed: {}".format(self.list_books.get_total_pages('c'))


    def required_book(self, sample):
        """
        This function shows how many pages to read and have a button for moving required book to completed book
        :param sample: kivy button
        :return: None
        """
        title = sample.text
        getBook = self.list_books.get_book_by_title(title)
        getBook.mark_book_completed()               # move required book to completed book
        self.top_label = "Total pages to read: {}".format(self.list_books.get_total_pages('r'))
        self.root.ids.displayBookList.remove_widget(widget=sample)

    def completed_book(self, sample):
        """
        This function displaying message for completed book
        :param sample: kivy button
        :return: None
        """
        title = sample.text
        completed_book = self.list_books.get_book_by_title(title)
        self.bottom_label = '{},(completed)'.format(completed_book)  # displaying message for completed book

    def book_button(self, mode):
        """
        This function highlights the button pressed by the clicks by users
        :param mode: "r" is required book and "c" is completed book.
                        This shows whether user clicked required book or completed book
        :return: None
        """
        if mode == "r":
            self.display_book_list(True)                        # shows required books
            self.root.ids.listRequired_button.state = 'down'    # state of button when required book is displayed
            self.root.ids.listCompleted_button.state = 'normal' # state of button when completed book is displayed
        elif mode == "c":
            self.display_book_list(False)                       # shows completed books
            self.root.ids.listRequired_button.state = 'normal'  # state of button when required book is displayed
            self.root.ids.listCompleted_button.state = 'down'   # state of button when completed book is displayed

    def clear_button(self):
        """
        This function delete the user input in "title", "author", and "page"
        :return: None
        """
        self.root.ids.title_of_book.text = ''
        self.root.ids.book_author.text = ''
        self.root.ids.number_of_page.text = ''

    def add_new_book(self, name_of_book, name_of_author, number_of_pages):
        """
        This function is for "add item" button for add a new book.
        Also, displays suitable message for each situation
        :param name_of_book: user input the "title" of new book
        :param name_of_author: user input the "author"
        :param number_of_pages: user input the number of "pages" of new book
        :return: None
        """

        try:                                            # Error checking
            count = 0
            for each in str(name_of_author):            # check whether there is no word in author name section
                if each not in (string.ascii_letters + ' '):
                    count += 1
            if count > 0:
                self.bottom_label = "Please enter valid author name, Author name cannot be a number"
            elif name_of_book == '' or name_of_book.isspace() or name_of_author == '' or name_of_author.isspace() or number_of_pages == '':
                self.bottom_label = "All filed must be completed"
            elif int(number_of_pages) <= 0:             # check whether there is no number in page section
                self.bottom_label = "Please enter a valid number"
            else:
                added_book = Book(name_of_book, name_of_author, int(number_of_pages), 'r')
                self.list_books.add_book(added_book)
                self.list_books.save_file()             # save a new book when a new book is added
                self.book_button("r")
                self.clear_button()
        except ValueError:                              # check whether there is invalid entry on page section
            self.bottom_label = "Please enter a valid number"

    def on_stop(self):
        print('Stop')
        self.list_books.save_file()                     # save changed or added books to the "books.csv" when the program finish

ReadingListApp().run()


