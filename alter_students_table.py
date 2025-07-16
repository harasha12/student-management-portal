import sqlite3

# Connect to your database file
conn = sqlite3.connect('students.db')
c = conn.cursor()

try:
    # Add the student_id column (if it doesn't exist)
    c.execute("ALTER TABLE students ADD COLUMN student_id TEXT ")
    print("✅ student_id column added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Error occurred:", e)

conn.commit()
conn.close()
