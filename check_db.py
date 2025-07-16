import sqlite3

# Connect to the correct database file
conn = sqlite3.connect('students.db')  # Make sure it's the one your Flask app uses
cursor = conn.cursor()

# Check existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("📋 Tables in the database:", tables)

# Check if 'grades' table exists and list its data
if ('grades',) in tables:
    cursor.execute("SELECT * FROM grades")
    records = cursor.fetchall()
    print("\n📚 Data in 'grades' table:")
    for row in records:
        print(row)
else:
    print("\n❌ 'grades' table does not exist.")

conn.close()