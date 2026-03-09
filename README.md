# Library Management System

# Pre-Description:
  This project is a console-based Library Management System developed in Python. The system simulates how a small library manages its books and user interactions.
  The program allows users to add books, view available books, borrow books, return books, and automatically calculate overdue penalties for late returns. All book data is saved to a file so that the information can be preserved between program executions.
  This project demonstrates the use of object-oreiented programming concepts, includingg classes, inheritance, encapsulation, and polymorphism, as well as file handling and exception handling in Python.

# Features:
• Add new books to the library 

• View all books in the system

• Borrow books

• Return books

• Automatic overdue penalty calculation

• Data persistence using text files

• Console-based user interaction

# Technologies Used:
• Python 3.11.5
• Object-Oriented Programming
• File Handling (.txt)
• Exception Handling

# Program Structure:
• Book
Represents a library book and stores information such as title, author, ISBN, availability status, borrow date, and due date.

• EBook
A subclass of Book that demonstrates inheritance and polymorephism.

• User
Represent a user who can borrow and return books.

• Library
Manages the collection of books and provides operations such as adding, viewing, and searching books.

• Filemanager
Handles saving and loading book data from a text file.

# Example Menu:
====== Library Management System ======
1. Add Book
2. View Books
3. Borrow Book
4. Return Book
5. Save and Exit
Choose an option:

# Example Data Storage:
Books are stored in books.txt in the following format:
Title, Author, ISBN, Availability
Python Basics, John Smith, 12345, True

# Future Improvements
• Add multiple user accounts

• Implement book search by author or ISBN

• Add due date reminders

• Create a graphical user interface (GUI)

• Implement a database instead of text files

