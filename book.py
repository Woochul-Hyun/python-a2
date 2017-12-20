class Book:
    def __init__(self, title="", author="", pages=0, status=""):
        """ This function is used to construct the Book class"""
        self.title = title
        self.author = author
        self.pages = pages
        self.status = status

    def __str__(self):
        """
        This function is used to display details such as book title, author, pages
        :return: book details including title of book, author, number of pages
        """
        return "{} by {},total pages is {}".format(self.title, self.author, self.pages)

    def mark_book_completed(self):
        """
        This function moves required book to completed book section
        """
        self.status = 'c'

    def longBook(self):
        """
        This functions checks whether number of page of book is over (or same) 500 or not
        :return: Ture or False
        """
        if self.pages >= 500:
            return True
        else:
            return False