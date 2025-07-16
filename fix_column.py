import sqlite3

# Connect to the database file
conn = sqlite3.connect('student_management.db')  # Make sure this is the correct DB file name
cursor = conn.cursor()

# Add the missing column if it doesn't exist
try:
    cursor.execute("ALTER TABLE grades ADD COLUMN student_name TEXT")
    print("✅ Column 'student_name' added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Error:", e)

conn.commit()
conn.close()