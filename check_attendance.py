import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM attendance").fetchall()

for row in rows:
    print(dict(row))

conn.close()
