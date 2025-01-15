import sqlite3

# Connect to the database (creates a file-based database)
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()

# Create a table for clients
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    mac_address TEXT NOT NULL UNIQUE,
    nickname TEXT,
    shutdown INTEGER NOT NULL, -- Use INTEGER for boolean values
    updatable_programs TEXT
)
''')

# Create a table for installed programs
cursor.execute('''
CREATE TABLE IF NOT EXISTS installed_programs (
    id INTEGER PRIMARY KEY,
    client_uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    current_version TEXT,
    available_version TEXT,
    FOREIGN KEY(client_uuid) REFERENCES clients(uuid) -- Add foreign key constraint
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

# Insert data into installed_programs
cursor.execute('''
INSERT INTO installed_programs (client_uuid, name, current_version) 
VALUES (?, ?, ?)
''', ('123e4567-e89b-12d3-a456-426614174000', 'Test Program', '1.0'))

# Insert data into clients
cursor.execute('''
INSERT INTO clients (uuid, mac_address, nickname, shutdown) 
VALUES (?, ?, ?, ?)
''', ('123e4567-e89b-12d3-a456-426614174000', '0x010000000000', 'testing PC', 0))

# Commit and close
conn.commit()
conn.close()
