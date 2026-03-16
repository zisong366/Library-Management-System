import tkinter as tk
from tkinter import ttk, messagebox
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
        self.borrower_id = None

    def borrow(self, person_id):
        if self.available:
            self.available = False
            self.borrower_id = person_id
            self.borrow_date = datetime.now()
            self.due_date = self.borrow_date + timedelta(days = 14)
            return True
        return False

    def return_book(self):
        penalty = self.calculate_penalty()
        self.available = True
        self.borrow_date = None
        self.due_date = None
        self.borrower_id = None
        return penalty

    def calculate_penalty(self):
        if self.due_date and datetime.now() > self.due_date:
            late_days = (datetime.now() - self.due_date).days
            return late_days * 1
        return 0

    def get_status(self):
        return "Available" if self.available else "Borrowed"
    
    def get_penalty(self):
        return self.calculate_penalty() if not self.available else 0

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
        with open("books.txt", "w", encoding = "utf-8") as file:
            for book in self.books:
                borrower_id = book.borrower_id if book.borrower_id else ""
                borrow_date = book.borrow_date.strftime("%Y-%m-%d %H:%M:%S") if book.borrow_date else ""
                due_date = book.due_date.strftime("%Y-%m-%d %H:%M:%S") if book.due_date else ""
                file.write(f"{book.title},{book.author},{book.isbn},{book.available},{borrower_id},{borrow_date},{due_date}\n")


    def load_books(self):
        books = []
        try:
            with open("books.txt", "r", encoding = "utf-8") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 7:
                        title, author, isbn, available, borrower_id, borrow_date, due_date = parts
                        book = Book(title.strip(), author.strip(), isbn.strip())
                        book.available = available.strip() == "True"
                        book.borrower_id = borrower_id.strip() if borrower_id.strip() else None
                        
                        if borrow_date:
                            book.borrow_date = datetime.strptime(borrow_date.strip(), "%Y-%m-%d %H:%M:%S")
                        
                        if due_date:
                            book.due_date = datetime.strptime(due_date.strip(), "%Y-%m-%d %H:%M:%S")

                        books.append(book)
        except FileNotFoundError:
            pass
        return books


library = Library()


# ------------------------------
# GUI Functions
def update_status(message):
    status_var.set(message)

def valid_person_id(person_id):
    return person_id.isdigit() and len(person_id) == 6


def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    person_entry.delete(0, tk.END)
    history_list.delete(0, tk.END)
    update_status("Fields cleared.")


def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if title and author and isbn:
        if library.find_book(title):
            messagebox.showwarning("Duplicate Book", "A book with this title already exists.")
            update_status("Book already exists.")
            return

        book = Book(title, author, isbn)
        library.add_book(book)
        library.save_books()
        view_books()
        clear_fields()
        messagebox.showinfo("Success", "Book added successfully!")
        update_status("Book added successfully.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        update_status("Failed to add book.")


def view_books(filtered_books = None):
    for row in book_table.get_children():
        book_table.delete(row)
    
    books_to_show = filtered_books if filtered_books is not None else library.books
    
    print("Books to show:", len(books_to_show))   # debug line

    for book in books_to_show:
        due = book.due_date.strftime("%Y-%m-%d") if book.due_date else "-"
        penalty_value = book.get_penalty()
        penalty = f"${penalty_value}"
        borrower = book.borrower_id if book.borrower_id else "-"

        # Determine row color
        if penalty_value > 0:
            tag = "overdue"
        elif not book.available:
            tag = "borrowed"
        else:
            tag = "available"

        book_table.insert(
            "",
            tk.END,
            values = (book.title, 
                      book.author, 
                      book.isbn, 
                      borrower, 
                      book.get_status(), 
                      due, 
                      penalty
                    ),
            tags = (tag,)
        )

    update_status("Book list refreshed.")

def search_books():
    keyword = search_entry.get().strip().lower()
    category = search_by.get()

    if not keyword:
        view_books()
        update_status("Showing all books.")
        return
    
    filtered = []

    for book in library.books:
        if category == "Title" and keyword in book.title.lower():
            filtered.append(book)
        elif category == "Author" and keyword in book.author.lower():
            filtered.append(book)
        elif category == "ISBN" and keyword in book.isbn.lower():
            filtered.append(book)
        elif category == "Borrower ID":
            borrower = book.borrower_id.lower() if book.borrower_id else ""
            if keyword in borrower:
                filtered.append(book)
        
    view_books(filtered)
    update_status(f"Found {len(filtered)} matching book(s).")

def reset_search():
    search_entry.delete(0, tk.END)
    search_by.set("Title")
    view_books()
    update_status("Search reset.")

def check_person_history():
    person_id = person_entry.get().strip()

    if not person_id:
        messagebox.showerror("Error","Please enter a Person ID.")
        update_status("Missing Person ID.")
        return
    
    if not valid_person_id(person_id):
        messagebox.showerror("Invalid ID","Person ID must be exactly 6 digits.")
        update_status("Invalid Person ID.")
        return
    
    history_list.delete(0, tk.END)

    found_books = []

    for book in library.books:
        if book.borrower_id == person_id:
            borrow_date = book.borrow_date.strftime("%Y-%m-%d %H:%M:%S") if book.borrow_date else "-"
            due_date = book.due_date.strftime("%Y-%m-%d") if book.due_date else "-"
            penalty = f"${book.get_penalty()}"

            record = f"{book.title} | {book.author} | {book.isbn} | Borrowed: {borrow_date} | Due: {due_date} | Penalty: {penalty}"
            found_books.append(record)

    if found_books:
        for item in found_books:
            history_list.insert(tk.END, item)

        messagebox.showinfo("Result", f"Found {len(found_books)} borrowed book(s).")
        update_status(f"Found {len(found_books)} borrowed book(s) for Person ID {person_id}.")
    else:
        history_list.insert(tk.END, "No currently borrowed books found for this Person ID.")

        messagebox.showinfo("Result", "No borrowed books found for this Person ID.")
        update_status("No borrowed books found for this Person ID.")


def borrow_book():
    title = title_entry.get().strip()
    person_id = person_entry.get().strip()

    if not title:
        messagebox.showerror("Error", "Please enter a book title.")
        update_status("Missing book title.")
        return
    
    if not person_id:
        messagebox.showerror("Error", "Please enter a Person ID.")
        update_status("Missing Person ID.")
        return
    
    if not valid_person_id(person_id):
        messagebox.showerror("Invalid ID", "Person ID must be exactly 6 digits.")
        update_status("Invalid Person ID.")
        return
    
    book = library.find_book(title)

    if book:
        if book.borrow(person_id):
            library.save_books()
            view_books()
            messagebox.showinfo("Success", "Book borrowed successfully!")
            update_status(f'"{book.title}" borrowed by ID {person_id}.')
        else:
            messagebox.showwarning("Unavailable", "This book is already borrowed.")   
            update_status(f'"{book.title}" is already borrowed.')   
    else:
        messagebox.showerror("Error", "Book not found.")
        update_status("Book not found.")


def return_book():
    title = title_entry.get().strip()
    book = library.find_book(title)

    if book:
        if book.available:
            messagebox.showwarning("Warning", "This book is already available.")
            update_status(f'"{book.title}" is already available.')
            return

        penalty = book.return_book()
        library.save_books()
        view_books()

        if penalty > 0:
            messagebox.showinfo("Late Return", f'Book returned successfully.\nLate return penalty: ${penalty}')
            update_status(f'"{book.title}" returned with penalty ${penalty}.')
        else:
            messagebox.showinfo("Success", "Book returned on time. No penalty")
            update_status(f'"{book.title}" returned on time.')
    else:
        messagebox.showerror("Error", "Book not found.")
        update_status("Book not found.")


def save_and_exit():
    library.save_books()
    root.destroy()


def on_row_select(event):
    selected = book_table.focus()
    if selected:
        values = book_table.item(selected, "values")
        if values:
            clear_entries_only()
            title_entry.insert(0, values[0])
            author_entry.insert(0, values[1])
            isbn_entry.insert(0, values[2])
            if values[3] != "-":
                person_entry.insert(0, values[3])
            update_status(f'Selected book: "{values[0]}"')


def clear_entries_only():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    person_entry.delete(0, tk.END)
    history_list.delete(0, tk.END)


# ------------------------------
# Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("1100x720")
root.configure(bg = "#F5F7FA")
root.resizable(False, False)

# ------------------------------
# ttk Style
style = ttk.Style()
style.theme_use("clam")

style.configure("Title.TLabel",
                font = ("Segoe UI", 20, "bold"),
                foreground = "#1E3A5F",
                background = "#F5F7FA")

style.configure("Subtitle.TLabel",
                font=("Segoe UI", 10),
                foreground = "#5B6B7A",
                background = "#F5F7FA")

style.configure("Custom.TLabelframe",
                background = "#F5F7FA")

style.configure("Custom.TLabelframe.Label",
                font = ("Segoe UI", 11, "bold"),
                foreground = "#1E3A5F",
                background = "#F5F7FA")

style.configure("TLabel",
                font = ("Segoe UI", 10),
                background = "#F5F7FA")

style.configure("TButton",
                font = ("Segoe UI", 10),
                padding=6)

style.configure("Treeview",
                font = ("Segoe UI", 10),
                rowheight = 28,
                foreground = "black",
                background = "white",
                fieldbackground = "white"
                )

style.configure("Treeview.Heading",
                font = ("Segoe UI", 10, "bold"))

# ------------------------------
# Header
header_frame = tk.Frame(root, bg = "#F5F7FA")
header_frame.pack(fill = "x", padx = 20, pady = (20, 10))

title_label = ttk.Label(header_frame, text="Library Management System", style="Title.TLabel")
title_label.pack()

subtitle_label = ttk.Label(
    header_frame,
    text = "Manage books, borrowing, and returns in a cleaner interface",
    style = "Subtitle.TLabel"
)
subtitle_label.pack(pady = (4, 0))

# ------------------------------
# Top Section
top_frame = tk.Frame(root, bg = "#F5F7FA")
top_frame.pack(fill = "x", padx = 20, pady = 10)

# Left: Book Information
info_frame = ttk.LabelFrame(top_frame, text = "Book Information", style = "Custom.TLabelframe")
info_frame.pack(side = "left", fill = "both", expand = True, padx = (0, 10), ipady = 10)

ttk.Label(info_frame, text = "Title:").grid(row = 0, column = 0, padx = 12, pady = 10, sticky = "e")
title_entry = ttk.Entry(info_frame, width = 30)
title_entry.grid(row = 0, column = 1, padx = 12, pady = 10, sticky = "w")

ttk.Label(info_frame, text="Author:").grid(row = 1, column = 0, padx = 12, pady = 10, sticky = "e")
author_entry = ttk.Entry(info_frame, width = 30)
author_entry.grid(row = 1, column = 1, padx = 12, pady = 10, sticky = "w")

ttk.Label(info_frame, text = "ISBN:").grid(row = 2, column = 0, padx = 12, pady = 10, sticky = "e")
isbn_entry = ttk.Entry(info_frame, width = 30)
isbn_entry.grid(row = 2, column = 1, padx = 12, pady = 10, sticky = "w")

ttk.Label(info_frame, text = "Person ID:").grid(row = 3, column = 0, padx = 12, pady = 10, sticky = "e")
person_entry = ttk.Entry(info_frame, width = 30)
person_entry.grid(row = 3, column = 1, padx = 12, pady = 10, sticky= "w")

# Right: Quick Actions
action_frame = ttk.LabelFrame(top_frame, text = "Quick Actions", style = "Custom.TLabelframe")
action_frame.pack(side = "right", fill = "y", ipadx = 10, ipady = 10)

ttk.Button(action_frame, text = "Add Book", width = 18, command = add_book).grid(row = 0, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "View Books", width = 18, command = view_books).grid(row = 1, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "Borrow Book", width = 18, command = borrow_book).grid(row = 2, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "Return Book", width = 18, command = return_book).grid(row = 3, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "Check Person ID", width = 18, command = check_person_history).grid(row = 4, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "Clear Fields", width = 18, command = clear_fields).grid(row = 5, column = 0, padx = 10, pady = 8)
ttk.Button(action_frame, text = "Save & Exit", width = 18, command = save_and_exit).grid(row = 6, column = 0, padx = 10, pady = 8)

# ------------------------------
# Bottom Section - Table
table_frame = ttk.LabelFrame(root, text = "Library Records", style = "Custom.TLabelframe")
table_frame.pack(fill = "both", expand = True, padx = 20, pady = (5, 10))

search_frame = tk.Frame(root, bg = "#F5F7FA")
search_frame.pack(fill = "x", padx = 20, pady = (5, 15))

ttk.Label(search_frame, text = "Search:").pack(side = "left", padx = (0, 8))

search_entry = ttk.Entry(search_frame, width = 30)
search_entry.pack(side = "left", padx = (0, 10))

search_by = ttk.Combobox(search_frame, values = ["Title", "Author", "ISBN", "Borrower ID"], state = "readonly", width = 15)
search_by.pack(side = "left", padx = (0, 10))
search_by.set("Title")

ttk.Button(search_frame, text = "Search" , command = search_books).pack(side = "left", padx = (0, 8))
ttk.Button(search_frame, text = "Reset" , command = reset_search).pack(side = "left")


columns = ("Title", "Author", "ISBN", "Borrower ID", "Status", "Due Date", "Penalty")
book_table = ttk.Treeview(table_frame, columns = columns, show = "headings", height = 12)
book_table.tag_configure("available", background = "#d4edda")
book_table.tag_configure("borrowed", background = "#fff3cd")
book_table.tag_configure("overdue", background = "#f8d7da")

for col in columns:
    book_table.heading(col, text = col, anchor = "center")

book_table.column("Title", width = 180, anchor = "center", stretch = True)
book_table.column("Author", width = 150, anchor = "center", stretch = True)
book_table.column("ISBN", width = 130, anchor = "center", stretch = True)
book_table.column("Borrower ID", width = 110, anchor = "center", stretch = True)
book_table.column("Status", width = 100, anchor = "center", stretch = True)
book_table.column("Due Date", width = 120, anchor = "center", stretch = True)
book_table.column("Penalty", width = 90, anchor = "center", stretch = True)

scrollbar = ttk.Scrollbar(table_frame, orient = "vertical", command = book_table.yview)
book_table.configure(yscrollcommand=scrollbar.set)

book_table.pack(side = "left", fill = "both", expand = True, padx = (10, 0), pady = 10)
scrollbar.pack(side = "right", fill = "y", padx = (0, 10), pady = 10)

book_table.bind("<<TreeviewSelect>>", on_row_select)

# ------------------------------
# Person ID Borrow History Section
history_frame = ttk.LabelFrame(root, text = "Person ID Borrowed Books", style = "Custom.TLabelframe")
history_frame.pack(fill = "both", expand = False, padx = 20, pady = (0, 10))

history_scrollbar = ttk.Scrollbar(history_frame, orient = "vertical")
history_scrollbar.pack(side = "right" , fill = "y", padx = (0, 10), pady = 10)

history_list = tk.Listbox(
    history_frame,
    height = 6,
    width = 120,
    yscrollcommand= history_scrollbar.set,
    font = ("Segoe UI", 10)
)
history_list.pack(side = "left", fill = "both", expand = True, padx = (10, 0), pady = 10)

history_scrollbar.config(command = history_list.yview)


# ------------------------------
# Status Bar
status_var = tk.StringVar()
status_var.set("Welcome to the Library Management System.")

status_bar = tk.Label(
    root,
    textvariable = status_var,
    bd = 1,
    relief = "sunken",
    anchor =  "w",
    font = ("Segoe UI", 9),
    bg = "#EAECEF",
    fg = "#2F3E4E",
    padx = 10
)
status_bar.pack(side = "bottom", fill = "x")

# ------------------------------
# Load books on start
view_books()

root.mainloop()