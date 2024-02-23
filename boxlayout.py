import sqlite3

# Connect to SQLite Database (it will create the database if it doesn't exist)
conn = sqlite3.connect('data.db')

# Create cursor
cur = conn.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS records
               (id INTEGER PRIMARY KEY, data TEXT)''')

# Commit changes and close
conn.commit()
conn.close()
