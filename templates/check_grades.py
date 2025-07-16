import sqlite3

conn = sqlite3.connect('students.db')
c = conn.cursor()

try:
    c.execute("SELECT * FROM grades")
    rows = c.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No grades found in the table.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.close()