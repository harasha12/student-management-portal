import sqlite3

# Connect to your database
conn = sqlite3.connect('students.db')
c = conn.cursor()

try:
    # Step 1: Rename the old grades table
    c.execute('ALTER TABLE grades RENAME TO grades_old;')

    # Step 2: Create new grades table with student_id as TEXT
    c.execute('''
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            subject TEXT,
            grade TEXT
        );
    ''')

    # Step 3: Copy data from old table using student_id from students table
    c.execute('''
        INSERT INTO grades (student_id, subject, grade)
        SELECT students.student_id, grades_old.subject, grades_old.grade
        FROM grades_old
        JOIN students ON grades_old.student_id = students.id;
    ''')

    # Step 4: Drop the old table
    c.execute('DROP TABLE grades_old;')

    conn.commit()
    print("✅ Migration completed successfully!")

except Exception as e:
    print("❌ Error:", e)

finally:
    conn.close()