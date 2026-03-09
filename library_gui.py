import tkinter as tk
from tkinter import messagebox 
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
            self.due_date =self.borrow_date + timedelta(days=14)
            return True
        return False
    
    def return_book(self):
        penalty = self.calculate_penalty()
        self.available = True
        self.borrow_date = None
        self.due_date = None
        return penalty
    
    def calculate_penalty(self):
        if self.due_date and datetime.now() > self.due_date:
            late_days = (datetime.now() - self.due_date).days
            return late_days * 1
        return 0
    
    def display_info(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} | {self.author} | {self.isbn} | {status}"
    
# ------------------------------
# Library Class
class Library:
    
    def __init__(self):
        self.books = self.load_books()

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def save_books(self):
        with open("books.txt", "w") as file:
            for book in self.books:
                file.write(f"{book.title},{book.author},{book.isbn}, {book.available}\n")
    
    def load_books(self):
        books = []
        try:
            with open("books.txt", "r") as file:
                for line in file:
                    title, author, isbn, available = line.strip().split(",")
                    book = Book(title, author, isbn)
                    book.available = available == "True"
                    books.append(book)
        except:
            pass
        return books

library = Library()            

#------------------------------
# GUI Functions
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()

    if title and author and isbn:
        book = Book(title, author, isbn)
        library.add_book(book)
        library.save_books()
        messagebox.showinfo("Success", "Book added successfully!")
        clear_fields()
        view_books()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def view_books():
    book_list.delete(0, tk.END)

    for book in library.books:
        book_list.insert(tk.END, book.display_info())

def borrow_book():
    title = title_entry.get()
    book = library.find_book(title)

    if book:
        if book.borrow():
            messagebox.showinfo("Success", "Book borrowed successfully!")
        else:
            messagebox.showwarning("Unavailable", "This book is already borrowed.")
    else:
        messagebox.showerror("Error", "Book not found.")

    view_books()

def return_book():
    title = title_entry.get()
    book = library.find_book(title)

    if book:
        penalty = book.return_book()

        if penalty > 0:
            messagebox.showinfo("Late Return", f"Book returned. Penalty: ${penalty}")
        else:
            messagebox.showinfo("Success", "Book returned on time.")

    else:
        messagebox.showerror("Error", "Book not found.") 

    view_books()

def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

def save_and_exit():
    library.save_books()
    root.destroy()

#------------------------------
# GUI Layout
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x450")

title_label = tk.Label(root, text = "Library Management System", font = ("Arial", 16))
title_label.pack(pady = 10)

# Input Fields
frame = tk.Frame(root)
frame.pack()

tk.Label(frame,text = "Title").grid(row = 0, column = 0)
title_entry = tk.Entry(frame)
title_entry.grid(row = 0, column = 1)

tk.Label(frame, text = "Author").grid(row = 1, column = 0 )
author_entry = tk.Entry(frame)
author_entry.grid(row = 1, column = 1)

tk.Label(frame, text = "ISBN").grid(row = 2, column = 0)
isbn_entry = tk.Entry(frame)
isbn_entry.grid(row = 2, column = 1)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady = 10)

tk.Button(button_frame, text = "Add Book", width = 15, command = add_book).grid(row = 0, column = 0, padx = 5)
tk.Button(button_frame, text = "View Books", width = 15, command = view_books).grid(row = 0, column = 1, padx = 5)
tk.Button(button_frame, text = "Borrow Book", width = 15, command = borrow_book).grid(row = 1, column = 0, padx = 5, pady = 5)
tk.Button(button_frame, text = "Return Book", width = 15, command = return_book).grid(row = 1, column = 1, padx = 5, pady = 5)
tk.Button(button_frame, text = "Clear Fields" , width = 15, command = clear_fields).grid(row = 2, column = 0, padx = 5)
tk.Button(button_frame, text = "Save & Exit", width = 15, command = save_and_exit).grid(row = 2, column = 1, padx = 5)

# Book List
list_frame = tk.Frame(root)
list_frame.pack(pady = 10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side = tk.RIGHT,fill = tk.Y)

book_list = tk.Listbox(list_frame, width = 80, yscrollcommand = scrollbar.set)
book_list.pack()

scrollbar.config(command = book_list.yview)

# Load books when program starts
view_books()

root.mainloop()