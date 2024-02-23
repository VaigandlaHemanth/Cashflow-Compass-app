import sqlite3
from sqlite3 import Error
import random
import datetime

def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table if it does not exist yet."""
    create_table_sql = '''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Category TEXT NOT NULL,
                            Account TEXT NOT NULL,
                            Amount REAL NOT NULL,
                            Type TEXT NOT NULL,
                            Date TEXT NOT NULL
                          );'''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_transaction(conn, transaction):
    """Insert a new transaction into the transactions table."""
    sql = '''INSERT INTO transactions(Category, Account, Amount, Type, Date)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid

def select_all_transactions(conn):
    """Query all rows in the transactions table, sorted by Date."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY Date")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def random_date(start, end):
    """Generate a random date between `start` and `end`."""
    time_between_dates = end - start
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def select_transactions_by_date(conn, search_date):
    """Query transactions by a specific date and return them as a list."""
    sql = '''SELECT * FROM transactions WHERE Date = ? ORDER BY Date'''
    cur = conn.cursor()
    cur.execute(sql, (search_date,))
    
    rows = cur.fetchall()
    
    transactions = []  # Initialize an empty list to store transactions
    for row in rows:
        transactions.append(row)
    
    return transactions


# Connect to SQLite DB: database will be created if it doesn't exist
conn = create_connection('mydatabase.db')

# Create transactions table
if conn is not None:
    create_table(conn)
else:
    print("Error! Cannot create the database connection.")

# Generate a random transaction with a random date
categories = ['Groceries', 'Utilities', 'Entertainment', 'Dining']
accounts = ['Checking', 'Savings','Debit', 'Credit']
types = ['Income', 'Expense','Transfer']
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime.now()

random_transaction = (
    random.choice(categories),
    random.choice(accounts),
    round(random.uniform(10, 500), 2),  # Random amount between 10 and 500
    random.choice(types),
    random_date(start_date, end_date)  # Random date
)

# Insert a random transaction
insert_transaction(conn, random_transaction)

# Query and print all transactions sorted by date
print("All transactions (sorted by date):")
select_all_transactions(conn)

# Close the database connection
conn.close()
