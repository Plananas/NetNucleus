import sqlite3

# Connect to the database (creates a file-based database)
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    mac_address TEXT NOT NULL UNIQUE,
    nickname TEXT,
    shutdown BOOLEAN NOT NULL,
    installed_programs TEXT,
    updatable_programs TEXT
)
''')

# Insert data
cursor.execute('''
INSERT INTO clients (mac_address, nickname, shutdown) VALUES (?, ?, ?)
''', ('0x010000000000', 'testing PC', False))

# Commit and close
conn.commit()
conn.close()
