import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database tables:")
for table in tables:
    print(f"- {table[0]}")

# Check if travel_customuser exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%customuser%';")
user_tables = cursor.fetchall()

print("\nCustom User tables:")
for table in user_tables:
    print(f"- {table[0]}")

conn.close()