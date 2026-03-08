from datetime import datetime, timedelta

# ------------------------------
# Book Class
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrow_date = None
        self.due_date = None

    def borrow(self):
        if self.available:
            self.available = False
            self.borrow_date = datetime.now()
            self.due_date = self.borrow_date + timedelta(days=14)
            print("Book borrowed sucessfully.")
            print("Due date:", self.due_date.date())
        else:
            print("Book is not available.")
    
    def return_book(self):
        penalty = self.calculate_penalty()
        self.available = True
        self.borrow_date = None
        self.due_date = None

        if penalty > 0:
            print(f"Book returned. Late penalty: ${penalty}")
        else:
            print("Book returned on time.")

    def calculate_penalty(self):
        if self.due_date and datetime.now() > self.due_date:
            late_days = (datetime.now() - self.due_date).days # Calculates how many days late the book is!
            return late_days * 1 # $1 per day
        return 0
    
    def display_info(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {status}"
    
# ------------------------------
# EBook Class
class EBook(Book):
    def __init__(self, title, author, isbn, file_size):
        super().__init__(title, author, isbn) # Calls the Book constructor
        self.file_size = file_size 

    def display_info(self):
        return f"{self.title} (EBook) by {self.author} | {self.file_size}MB"

# ------------------------------
# User Class
class User:
    def __init__ (self,name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.available:
            book.borrow()
            self.borrowed_books.append(book)
        else:
            print("Book not available for borrowing.")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
        else:
            print("This book was not borrowed by the user.")

# ------------------------------
# File Manager Class
class FileManager:
    @ staticmethod
    def save_books(books):
        with open("books.txt", "w") as file:
            for book in books:
                file.write(f"{book.title}, {book.author}, {book.isbn}, {book.available}\n")

    @ staticmethod
    def load_books():
        books = []
        try:
            with open("book.txt", "r") as file:
                for line in file:
                    title, author, isbn, available = line.strip().split(",") # Remove the spaces, and splits the line by commas.
                    book = Book(title, author, isbn)
                    book.available = available == "True"
                    books.append(book)
        except FileNotFoundError:
            print("No saved book data found.")

        return books
    
# ------------------------------
# Library Class
class Library:
    def __init__(self):
        self.books = FileManager.load_books() # Loads all saved books when the program starts.

    def add_book(self):
        try:
            title = input("Enter book title: ")
            author = input("Enter author name:")
            isbn = input("Enter ISBN number: ")

            book = Book(title, author, isbn)
            self.books.append(book)

            print("Book added successfully.")

        except Exception:
            print("Error adding book. Please try again.")

    def view_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books:
            print(book.display_info())

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
# ------------------------------
# Main Function
def main():
    library = Library()
    user = User("Guest")

    while True: # Crete an infinite loop to keep the program running until the user chooses to exit.
        print("\n====== Library Management System ======")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Save and Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                library.add_book()

            elif choice == "2":
                library.view_books()

            elif choice == "3":
                title = input("Enter the title of the book to borrow: ")
                book = library.find_book(title)

                if book:
                    user.borrow_book(book)
                else:
                    print("Book is not found.")

            elif choice == "4":    
                title = input("Enter the title of the book to return: ")
                book = library.find_book(title)

                if book:
                    user.return_book(book)
                else:
                    print("Book is not found.")

            elif choice == "5":
                FileManager.save_books(library.books)
                print("Books saved. Exiting the program.")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception:
            print("An error occurred:", Exception) # Catches any unexpected errors and prints the error message.

main()