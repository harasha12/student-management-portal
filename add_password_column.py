import sqlite3

def add_password_column_if_missing(table_name):
    conn = sqlite3.connect('students.db')  # Update with your DB path if different
    cursor = conn.cursor()

    # Check if 'password' column exists
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [column[1] for column in cursor.fetchall()]

    if 'password' not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN password TEXT;")
        print(f"✅ Added 'password' column to '{table_name}' table.")
    else:
        print(f"ℹ️ 'password' column already exists in '{table_name}' table.")

    conn.commit()
    conn.close()

# Run for both tables
add_password_column_if_missing("students")
add_password_column_if_missing("teachers")
