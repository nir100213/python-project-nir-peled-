from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Configure SQLite database
DATABASE = 'database.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Books (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Author TEXT, YearPublished INTEGER, Type INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Customers (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, City TEXT, Age INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Loans (CustID INTEGER, BookID INTEGER, LoanDate TEXT, ReturnDate TEXT, FOREIGN KEY (CustID) REFERENCES Customers(Id), FOREIGN KEY (BookID) REFERENCES Books(Id))")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Retrieve data from tables
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Loans")
    loans = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', books=books, customers=customers, loans=loans)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customers (Name, City, Age) VALUES (?, ?, ?)", (name, email))
    conn.commit()
    conn.close()

    return 'User added successfully.'

@app.route('/add_book', methods=['POST'])
def add_book():
    book_name = request.form['book_name']
    author = request.form['author']
    year_published = request.form['year_published']
    book_type = request.form['type']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (Name, Author, YearPublished, Type) VALUES (?, ?, ?, ?)", (book_name, author, year_published, book_type))
    conn.commit()
    conn.close()

    return 'Book added successfully.'

@app.route('/add_customer', methods=['POST'])
def add_customer():
    customer_name = request.form['customer_name']
    city = request.form['city']
    age = request.form['age']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customers (Name, City, Age) VALUES (?, ?, ?)", (customer_name, city, age))
    conn.commit()
    conn.close()

    return 'Customer added successfully.'

@app.route('/add_loan', methods=['POST'])
def add_loan():
    customer_id = request.form['customer_id']
    book_id = request.form['book_id']
    loan_date = request.form['loan_date']
    return_date = request.form['return_date']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Loans (CustID, BookID, LoanDate, ReturnDate) VALUES (?, ?, ?, ?)", (customer_id, book_id, loan_date, return_date))
    conn.commit()
    conn.close()

    return 'Loan added successfully.'

@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form['book_id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE Id=?", (book_id,))
    conn.commit()
    conn.close()

    return 'Book deleted successfully.'

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    customer_id = request.form['customer_id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE Id=?", (customer_id,))
    conn.commit()
    conn.close()

    return 'Customer deleted successfully.'

@app.route('/delete_loan', methods=['POST'])
def delete_loan():
    customer_id = request.form['customer_id']
    book_id = request.form['book_id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Loans WHERE CustID=? AND BookID=?", (customer_id, book_id))
    conn.commit()
    conn.close()

    return 'Loan deleted successfully.'

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
