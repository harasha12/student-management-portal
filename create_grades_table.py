import sqlite3

# Connect to the database
conn = sqlite3.connect('student_management.db')  # Make sure this is the right file name
cursor = conn.cursor()

# Create the grades table
cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_name TEXT,
    subject TEXT,
    grade TEXT
)
''')

conn.commit()
conn.close()

print("✅ 'grades' table created successfully.")