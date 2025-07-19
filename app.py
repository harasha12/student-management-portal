import random

import html
import re
from flask_mail import Mail, Message

from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'harshavardhanvangara@gmail.com'       # replace with your email
app.config['MAIL_PASSWORD'] = 'bfllbazxsxinlheb'          # replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = 'harshavardhanvangara@gmail.com' # same as above
mail = Mail(app)


app.secret_key = 'your_secret_key'

from datetime import timedelta

app.permanent_session_lifetime = timedelta(minutes=20)  # Auto-logout after 20 minutes

DATABASE = 'students.db'

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize DB
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT,
                            course TEXT,
                            enrollment_date TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    date TEXT,
    period1 TEXT,
    period2 TEXT,
    period3 TEXT,
    period4 TEXT,
    period5 TEXT,
    period6 TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)
''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    subject TEXT,
                    grade TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                       UNIQUE (student_id,subject));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    receiver TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('teacher', 'student')) NOT NULL DEFAULT 'student'
                    )''')

        db.commit()

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


# Login
@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()

        # ✅ Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "Username already exists. Please choose another."
        else:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, hashed_password, role))
            conn.commit()
            conn.close()
            success = "Registration successful! Please login."
            if role == 'student':
                return redirect(url_for('student_login'))
            else:
                return redirect(url_for('teacher_login'))

    return render_template('register.html', role=role, error=error)


@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    error, success = None, None
    if request.method == 'POST':
        username = html.escape(request.form['username'])
        email = html.escape(request.form['email'])   # New line
        password = request.form['password']
        role = 'student'

        if len(password) < 6:
            error = "Password must be at least 6 characters."
        elif not re.search(r"\d", password):
            error = "Password must include a number."
        elif not re.search(r"[A-Z]", password):
            error = "Password must include an uppercase letter."
        elif not re.search(r"[!@#$%^&*()_+]", password):
            error = "Password must include a special character."
        else:
            db = get_db()
            try:
                db.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                           (username, email, generate_password_hash(password), role))
                db.commit()
                success = "Student registered successfully!"
            except sqlite3.IntegrityError:
                error = "Username already exists."

    return render_template('register.html', error=error, success=success)

import sqlite3

def create_internal_marks_table():
    conn = sqlite3.connect('your_database_name.db')  # Replace with your DB file name
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internal_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            internal_marks TEXT NOT NULL,
            entered_by TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ internal_marks table created.")

create_internal_marks_table()

@app.route('/create_internal_marks_table')
def create_internal_marks_table():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS internal_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            internal_marks TEXT NOT NULL,
            entered_by TEXT NOT NULL
        )
    ''')
    db.commit()
    return "✅ internal_marks table created successfully!"

@app.route('/')
def choose_login():
    return render_template('choose_login.html')
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND role = 'teacher'", (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user'] = user['username']
            session['role'] = 'teacher'
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid teacher credentials."
    return render_template('teacher_login.html', error=error)

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND role = 'student'", (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user'] = user['username']
            session['role'] = 'student'
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid student credentials."
    return render_template('student_login.html', error=error)

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (session['user'],)).fetchone()

    if user['role'] == 'teacher':
        return render_template('teacher_dashboard.html', user=user['username'])
    elif user['role'] == 'student':
        return render_template('student_dashboard.html', user=user['username'])
    else:
        return "Unauthorized", 403



# Add Student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))

    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        date = request.form['date']
        added_by = session.get('user') or 'unknown'
        db = get_db()

        try:
            db.execute(
                "INSERT INTO students (student_id, name, email, course, enrollment_date, added_by) VALUES (?, ?, ?, ?, ?, ?)",
                (student_id, name, email, course, date, added_by)
            )
            db.commit()
            return redirect(url_for('view_students'))
        except sqlite3.IntegrityError:
            return "Student ID already exists."

    return render_template('add_student.html')



# View Students
@app.route('/students')
def view_students():
    if 'user' not in session:
        return redirect('/')
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    return render_template('view_students.html', students=students)
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))
    
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        enrollment_date = request.form['enrollment_date']

        db.execute("UPDATE students SET name=?, email=?, course=?, enrollment_date=? WHERE id=?",
                   (name, email, course, enrollment_date, id))
        db.commit()
        return redirect(url_for('view_students'))

    student = db.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))

    db = get_db()

    # Step 1: Get the student_id using internal ID
    student = db.execute("SELECT student_id FROM students WHERE id = ?", (id,)).fetchone()

    if student:
        student_id = student['student_id']

        # Step 2: Delete attendance records first
        db.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))

        # Step 3: Delete student from the students table
        db.execute("DELETE FROM students WHERE id = ?", (id,))
        
        db.commit()

    return redirect(url_for('view_students'))


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Mark Attendance

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))

    db = get_db()
    teacher_username = session['user']
    students = db.execute("SELECT student_id, name FROM students WHERE added_by = ?", (teacher_username,)).fetchall()

    selected_period = None

    if request.method == 'POST':
        date = request.form['date']
        selected_period = request.form['selected_period']

        for student in students:
            student_id = student["student_id"]
            remarks = request.form.get(f'remarks_{student_id}', '')

            # NEW: Use a fixed name so HTML always works
            status_value = request.form.get(f'status_{student_id}', 'Absent')

            # Prepare blank periods
            period_data = {f'period{i}': None for i in range(1, 7)}
            period_data[f'period{selected_period}'] = status_value

            existing = db.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, date)).fetchone()

            if existing:
                db.execute(f"""
                    UPDATE attendance
                    SET period{selected_period} = ?, remarks = ?
                    WHERE student_id = ? AND date = ?
                """, (status_value, remarks, student_id, date))
            else:
                db.execute("""
                    INSERT INTO attendance (student_id, date, period1, period2, period3, period4, period5, period6, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    student_id, date,
                    period_data['period1'],
                    period_data['period2'],
                    period_data['period3'],
                    period_data['period4'],
                    period_data['period5'],
                    period_data['period6'],
                    remarks
                ))

        db.commit()
        return redirect(url_for('view_attendance'))

    return render_template('mark_attendance.html', students=students, selected_period=selected_period)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']  # 🆕 get selected role
        db = get_db()

        if role == 'student':
            cur = db.execute("SELECT email FROM students WHERE student_id = ?", (username,))
        else:
            cur = db.execute("SELECT email FROM teachers WHERE teacher_id = ?", (username,))

        user = cur.fetchone()

        if user:
            email = user['email']
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            session['reset_username'] = username
            session['reset_role'] = role  # 🆕 also store role for later

            # Send OTP
            msg = Message('Your OTP Code', recipients=[email])
            msg.body = f'Your OTP is: {otp}'
            mail.send(msg)

            return redirect(url_for('verify_otp'))
        else:
            error = "No account found with that username."

    return render_template('forgot_password.html', error=error)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    error, success = None, None

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            error = "Passwords do not match."
        elif len(new_password) < 6:
            error = "Password must be at least 6 characters."
        else:
            hashed_pw = generate_password_hash(new_password)
            username = session.get('reset_username')
            role = session.get('reset_role')  # 🔁 Retrieve role (student or teacher)

            db = get_db()

            if role == 'student':
                db.execute("UPDATE students SET password = ? WHERE student_id = ?", (hashed_pw, username))
            elif role == 'teacher':
                db.execute("UPDATE teachers SET password = ? WHERE teacher_id = ?", (hashed_pw, username))
            else:
                error = "Invalid user role."
                return render_template('reset_password.html', error=error)

            db.commit()
            success = "Password reset successful! Redirecting to login..."
            return redirect(url_for('student_login') if role == 'student' else url_for('teacher_login'))

    return render_template('reset_password.html', error=error, success=success)

# View Attendance
@app.route('/view_attendance')
def view_attendance():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect('/')

    db = get_db()
    teacher_username = session['user']

    records = db.execute('''
        SELECT s.student_id, s.name, a.date,
               a.period1, a.period2, a.period3, a.period4, a.period5, a.period6, a.remarks
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        WHERE s.added_by = ?
        ORDER BY a.date DESC
    ''', (teacher_username,)).fetchall()

    # Count total Present and Absent from all period columns
    # Count total Present and Absent from all period columns (with case-insensitive comparison)
    total_present = 0
    total_absent = 0
    for row in records:
     for i in range(1, 7):
        value = row[f'period{i}']
        if value and value.strip().lower() == 'present':
            total_present += 1
        elif value and value.strip().lower() == 'absent':
            total_absent += 1

    return render_template('view_attendance.html',
                           records=records,
                           total_present=total_present,
                           total_absent=total_absent)


@app.route('/student_view_attendance')
def student_view_attendance():
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('choose_login'))

    db = get_db()
    student_id = session['user']  # or session['user'] if you're storing student_id there
    attendance = db.execute("SELECT * FROM attendance WHERE student_id = ?", (student_id,)).fetchall()
    return render_template('student_view_attendance.html', attendance=attendance)
    session['user'] = student['student_id']

    # Count totals
    total_present = sum(1 for r in records if r['status'] == 'Present')
    total_absent = sum(1 for r in records if r['status'] == 'Absent')

    return render_template(
        'view_attendance.html',
        records=records,
        total_present=total_present,
        total_absent=total_absent
    )

from fpdf import FPDF
from flask import make_response

@app.route('/download_attendance_pdf')
def download_attendance_pdf():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect('/')

    db = get_db()
    records = db.execute('''SELECT s.name, a.date, a.status
                            FROM attendance a
                            JOIN students s ON a.student_id = s.id
                            ORDER BY a.date DESC''').fetchall()

    summary = {}
    total_present = 0
    total_absent = 0

    for record in records:
        name = record['name']
        status = record['status']
        if name not in summary:
            summary[name] = {'Present': 0, 'Absent': 0}
        summary[name][status] += 1

        # Count total
        if status == "Present":
            total_present += 1
        elif status == "Absent":
            total_absent += 1

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, " Attendance Summary", ln=True, align='C')
    pdf.ln(10)

    for name, counts in summary.items():
        pdf.cell(200, 10, f"{name} - Present: {counts['Present']}, Absent: {counts['Absent']}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Total Present Entries: {total_present}", ln=True)
    pdf.cell(200, 10, f"Total Absent Entries: {total_absent}", ln=True)

    # Generate response
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition', 'attachment', filename='attendance_summary.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response
from datetime import datetime, timedelta

@app.route('/attendance_percentage')
def attendance_percentage():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect('/')

    db = get_db()
    teacher_username = session['user']

    six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')

    records = db.execute("""
        SELECT s.student_id, s.name,
               COUNT(a.status) AS total_days,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days
        FROM students s
        LEFT JOIN attendance a ON s.student_id = a.student_id
            AND a.date >= ?
        WHERE s.added_by = ?
        GROUP BY s.student_id
    """, (six_months_ago, teacher_username)).fetchall()

    # Calculate percentage
    result = []
    for row in records:
        percentage = 0
        if row['total_days']:
            percentage = round((row['present_days'] or 0) / row['total_days'] * 100, 2)
        result.append({
            'student_id': row['student_id'],
            'name': row['name'],
            'percentage': percentage,
            'present_days': row['present_days'] or 0,
            'total_days': row['total_days']
        })

    return render_template('attendance_percentage.html', data=result)
from flask import request
from datetime import datetime, timedelta

@app.route('/custom_attendance_percentage', methods=['GET', 'POST'])
def custom_attendance_percentage():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect('/')

    db = get_db()
    teacher_username = session['user']
    data = []
    start_date, end_date = None, None

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        records = db.execute("""
            SELECT s.student_id, s.name,
                   COUNT(a.status) AS total_days,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days
            FROM students s
            LEFT JOIN attendance a ON s.student_id = a.student_id
                AND a.date BETWEEN ? AND ?
            WHERE s.added_by = ?
            GROUP BY s.student_id
        """, (start_date, end_date, teacher_username)).fetchall()

        for row in records:
            percentage = 0
            if row['total_days']:
                percentage = round((row['present_days'] or 0) / row['total_days'] * 100, 2)
            data.append({
                'student_id': row['student_id'],
                'name': row['name'],
                'percentage': percentage,
                'present_days': row['present_days'] or 0,
                'total_days': row['total_days']
            })

    return render_template('custom_attendance_percentage.html', data=data, start_date=start_date, end_date=end_date)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    error = None
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            return redirect(url_for('reset_password'))  # Next step
        else:
            error = "Invalid OTP. Please try again."

    return render_template('verify_otp.html', error=error)

@app.route('/internal_marks', methods=['GET', 'POST'])
def internal_marks():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))

    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    error = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        try:
            for i in range(1, 6):  # For 5 subjects
                subject = request.form.get(f'subject_{i}')
                marks = request.form.get(f'marks_{i}')
                if subject and marks:
                    db.execute("INSERT INTO internal_marks (student_id, subject, marks) VALUES (?, ?, ?)",
                               (student_id, subject, marks))
            db.commit()
            return redirect(url_for('view_internal_marks'))
        except sqlite3.IntegrityError:
            error = "Duplicate subject entry for this student is not allowed."

    return render_template('internal_marks.html', students=students, error=error)


@app.route('/enter_internal_marks', methods=['GET', 'POST'])
def enter_grade():
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))
    db = get_db()
    students = db.execute("SELECT id, name FROM students").fetchall()

    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        marks = request.form['marks']

        db.execute("INSERT INTO internal_marks (student_id, subject, marks) VALUES (?, ?, ?)",
                   (student_id, subject, marks))
        db.commit()
        return redirect('/view_internal_marks')

    return render_template('enter_internal_marks.html', students=students)



@app.route('/view_internal_marks', methods=['GET', 'POST'])
def view_internal_marks():
    if 'user' not in session:
        return redirect(url_for('choose_login'))

    db = get_db()
    role = session.get('role')
    user_id = session['user']

    if role == 'student':
        # Show only logged-in student's internal marks
        records = db.execute('''
            SELECT im.student_id, s.name AS student_name, im.subject, im.marks
            FROM internal_marks im
            JOIN students s ON im.student_id = s.student_id
            WHERE im.student_id = ?
        ''', (user_id,)).fetchall()

        return render_template('view_internal_marks.html', records=records)

    elif role == 'teacher':
        # Show filter form and all students' marks
        if request.method == 'POST':
            student_id = request.form.get('student_id')
            subject = request.form.get('subject')

            query = '''
                SELECT im.student_id, s.name AS student_name, im.subject, im.marks
                FROM internal_marks im
                JOIN students s ON im.student_id = s.student_id
                WHERE s.added_by = ?
            '''
            filters = []
            params = [user_id]  # teacher who added students

            if student_id:
                filters.append('im.student_id = ?')
                params.append(student_id)
            if subject:
                filters.append('im.subject LIKE ?')
                params.append(f'%{subject}%')

            if filters:
                query += ' AND ' + ' AND '.join(filters)

            records = db.execute(query, params).fetchall()
        else:
            records = db.execute('''
                SELECT im.student_id, s.name AS student_name, im.subject, im.marks
                FROM internal_marks im
                JOIN students s ON im.student_id = s.student_id
                WHERE s.added_by = ?
            ''', (user_id,)).fetchall()

        students = db.execute("SELECT student_id, name FROM students WHERE added_by = ?", (user_id,)).fetchall()
        return render_template('view_internal_marks.html', records=records, students=students)

    else:
        return redirect(url_for('choose_login'))


@app.route('/delete_internal_marks/<student_id>/<subject>')
def delete_internal_marks(student_id, subject):
    if 'user' not in session or session.get('role') != 'teacher':
        return redirect(url_for('choose_login'))

    db = get_db()
    db.execute("DELETE FROM internal_marks WHERE student_id = ? AND subject = ?", (student_id, subject))
    db.commit()
    return redirect(url_for('view_internal_marks'))


@app.route('/edit_internal_marks/<student_id>/<subject>', methods=['GET', 'POST'])
def edit_internal_marks(student_id, subject):
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'POST':
        new_marks = request.form['marks']
        c.execute("""
            UPDATE internal_marks
            SET internal_marks = ?
            WHERE student_id = ? AND subject = ?
        """, (new_marks, student_id, subject))
        conn.commit()
        conn.close()
        return redirect(url_for('view_internal_marks'))

    c.execute("""
        SELECT * FROM internal_marks
        WHERE student_id = ? AND subject = ?
    """, (student_id, subject))
    row = c.fetchone()
    conn.close()

    return render_template('edit_internal_marks.html',
                           student_id=student_id,
                           subject=subject,
                           marks=row['marks'])

# Send Message

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'user' not in session:
        return redirect('/')
    
    db = get_db()

    # Get list of users (only students if teacher is logged in)
    if session.get('role') == 'teacher':
        users = db.execute("SELECT username FROM users WHERE role = 'student'").fetchall()
    else:
        users = db.execute("SELECT username FROM users WHERE role = 'teacher'").fetchall()

    if request.method == 'POST':
        receiver = request.form['receiver']
        message = request.form['message']

        db.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
                   (session['user'], receiver, message))
        db.commit()
        return redirect(url_for('inbox'))

    return render_template('send_message.html', users=users)

# View Inbox
@app.route('/inbox')
def inbox():
    if 'user' not in session:
        return redirect('/')
    
    db = get_db()
    messages = db.execute("SELECT sender, message, timestamp FROM messages WHERE receiver = ? ORDER BY timestamp DESC", 
                          (session['user'],)).fetchall()
    
    return render_template('inbox.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)