# Project Overview

The Library Management System is a desktop application built using Python and Tkinter that provides a graphical interface for managing a small library collection.

The system allows users to:

  1. Add books to the library
  
  2. Borrow books using a Person ID
  
  3. Return books and automatically calculate late penalties
  
  4. Search books by different fields
  
  5. View borrowing history for a specific user

  6. Store and load records using a persistent text file

This project demonstrates the use of:

  1. Object-Oriented Programming (OOP)
  
  2. Graphical User Interface (GUI) design
  
  3. File-based data persistence
  
  4. Event-driven programming
  
  5. Data validation
     
# System Architecture

  The system follows a simple 3-layer architecture:
  
  +----------------------+
  |       GUI Layer      |
  |   (Tkinter Interface)|
  +----------▲-----------+
             |
             |
  +----------▼-----------+
  |     Logic Layer      |
  |  (Book & Library)    |
  +----------▲-----------+
             |
             |
  +----------▼-----------+
  |    Data Storage      |
  |      books.txt       |
  +----------------------+
  GUI Layer
  
  Handles user interaction:
  
   1. Buttons
  
   2. Input fields
  
   3. Table display
  
   4. Search
  
   5. History panel
  
  Logic Layer
  
  Contains system logic using classes:
  
   1. Book management
  
   2. Borrowing rules
  
   3. Penalty calculation
  
  Data Storage
  
  Data is saved in a text file:
  
   books.txt
  
  This allows the system to restore library records when the program restarts.

# Object-Oriented Design
3.1 Book Class

The Book class represents an individual book in the library.

Attributes
  Attribute          Description
  title	               Name of the book
  author	             Author name
  isbn	               Unique identifier
  available	           Availability status
  borrower_id	         Person who borrowed the book
  borrow_date	         Date when borrowed
  due_date	           Due date (14 days later)

Key Methods
borrow(person_id):
  Marks the book as borrowed and records the borrower.

return_book():
  Returns the book and calculates any penalty.

calculate_penalty():
  Determines overdue penalty based on late days.

Penalty rule:
  Penalty = $1 × number of overdue days

  
3.2 Library Class

The Library class manages the collection of books.

Responsibilities:
  1. Load books from file
  
  2. Save books to file
  
  3. Add new books
  
  4. Search for books

Key Methods
  Method	            Purpose
  add_book()	        Adds new book
  find_book()	        Finds book by title
  save_books()	      Saves data to file
  load_books()	      Loads records at startup
  
# Graphical User Interface (GUI)

  The GUI is built using Tkinter with ttk styling.
  
  The interface is divided into several sections:
  
  -----------------------------------------------------
  |            Library Management System               |
  |---------------------------------------------------|
  | Book Information |        Quick Actions           |
  |---------------------------------------------------|
  |                 Search Bar                        |
  |---------------------------------------------------|
  |                Library Records Table              |
  |---------------------------------------------------|
  |              Borrow History Panel                 |
  |---------------------------------------------------|
  |                   Status Bar                      |
  -----------------------------------------------------
  
# Core Features
5.1 Add Book

  Users can add books by entering:
  
   1. Title
  
   2. Author
  
   3. ISBN
  
  The system prevents duplicate titles.

5.2 Borrow Book

  Books can be borrowed using a Person ID.
  
  Validation rules:
  
   1. Person ID must be exactly 6 digits
  
  When borrowed, the system records:
  
   1. Borrow date
  
   2. Due date (14 days)

5.3 Return Book

Returning a book triggers a penalty check.

If the book is overdue:

  Penalty = $1 × number of late days

Example:

  Due date: March 10
  Return date: March 15
  Penalty: $5

5.4 Library Records Table

The table displays:

Column	           Description
Title	             Book name
Author	           Author name
ISBN	             Book identifier
Borrower ID	       Current borrower
Status	           Available / Borrowed
Due Date	         Return deadline
Penalty	           Late fee

Row Colors
Color              Meaning
Green	             Available
Yellow	           Borrowed
Red	               Overdue

This improves visual readability for librarians.

5.5 Search Function

  Books can be searched by:
  
   1. Title
  
   2. Author
  
   3. ISBN
  
   4. Borrower ID
  
  The system filters results dynamically.

5.6 Borrow History

Users can check borrowed books using a Person ID.

  Displayed information includes:
  
   1. Book title
  
   2. Author
  
   3. ISBN
  
   4. Borrow date
  
   5. Due date
  
   6. Current penalty
      

# Data Storage Format

All records are stored in:

  books.txt

Example record:

Clean Code,Robert C. Martin,9780132350884,False,123456,2026-03-15 10:00:00,2026-03-29 10:00:00
Field	               Meaning
Title	               Book title
Author	             Author
ISBN	               Book identifier
Available	           True / False
Borrower ID	         Person ID
Borrow Date	         Date borrowed
Due Date	           Return deadline

# File Structure
  Final Project
  │
  
  ├── library_gui.py
  
  ├── books.txt
  
  └── README.md
  library_gui.py
  
  Main application including:
  
   1. Book class
  
   2. Library class
  
   3. GUI logic
  
books.txt
  
  Persistent storage for book records.
  
README.md
  
  Project documentation.

# How to Run the Program
Requirements:

Python 3.10+

  Tkinter (included with standard Python).

Run the program

Navigate to the project folder and run:

  python library_gui.py

The GUI window will open automatically.

# Example Usage

Example workflow:

 1. Add a new book

 2. Click View Books

 3. Enter a Person ID

 4. Click Borrow Book

 5. Use Check Person ID to see borrowing history

 6. Return the book using Return Book

# Possible Future Improvements

Potential enhancements include:

 1. SQLite database integration

 2. User authentication system

 3. Multiple copies of books

 4. Borrow history logging

 5. Barcode scanning

 6. Dark mode interface

 7. Exporting reports

# Technologies Used
  Technology	           Purpose
  Python	               Programming language
  Tkinter	               GUI framework
  ttk	                   Modern UI styling
  datetime	             Date calculations
  File I/O	             Data persistence

# Learning Outcomes

This project demonstrates understanding of:

  1. Object-Oriented Programming

  2. GUI application development

  3. Event-driven programming

  4. Data validation

  5. File-based data storage

  6. Python class design

# Author

  Library Management System developed as a final project for learning Python GUI development and Object-Oriented Programming concepts.
