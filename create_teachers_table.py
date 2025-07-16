import sqlite3

def create_teachers_table():
    conn = sqlite3.connect('students.db')  # Change path if needed
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='teachers';
    """)
    result = cursor.fetchone()

    if result:
        print("ℹ️ Table 'teachers' already exists.")
    else:
        cursor.execute("""
            CREATE TABLE teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT
            );
        """)
        conn.commit()
        print("✅ 'teachers' table created successfully.")

    conn.close()

create_teachers_table()
