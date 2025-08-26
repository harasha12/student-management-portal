BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY ,
    student_id TEXT,
    date TEXT,
    period1 TEXT,
    period2 TEXT,
    period3 TEXT,
    period4 TEXT,
    period5 TEXT,
    period6 TEXT,
    remarks TEXT, added_by TEXT, status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
CREATE TABLE IF NOT EXISTS faculty_uploads (
    id INT AUTO_INCREMENT PRIMARY KEY ,
    title TEXT,
    branch TEXT,
    filename TEXT,
    uploaded_by TEXT,
    file_type TEXT,
    upload_date TEXT
);
CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    subject TEXT,
                    grade TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                       UNIQUE (student_id,subject));
CREATE TABLE IF NOT EXISTS internal_marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    subject TEXT,
    marks INTEGER,
    semester TEXT,
    added_by TEXT
);
CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    receiver TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   );
CREATE TABLE IF NOT EXISTS "students" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT,
    added_by TEXT
, email TEXT, course TEXT, enrollment_date TEXT, username TEXT, password TEXT);
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('teacher', 'student')) NOT NULL DEFAULT 'student'
                    );
INSERT INTO "attendance" ("id","student_id","date","period1","period2","period3","period4","period5","period6","remarks","added_by","status") VALUES (1,'1133','2025-07-21','Present','Present',NULL,'Present','Present','Present','',NULL,NULL),
 (2,'23B81A4690','2025-07-21','Present','Present',NULL,'Present','Present','Present','',NULL,NULL),
 (4,'1133','2025-07-27','Absent','Present','Present',NULL,NULL,NULL,'',NULL,NULL),
 (5,'23B81A4690','2025-07-27','Present','Present','Present',NULL,NULL,NULL,'',NULL,NULL),
 (6,'1133','2025-07-28','Present',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (7,'23B81A4690','2025-07-28','Present',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (8,'23B81A4246','2025-07-28','Present',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (9,'1133','2025-07-15',NULL,'Present',NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (10,'23B81A4690','2025-07-15',NULL,'Present',NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (11,'23B81A4246','2025-07-15',NULL,'Present',NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (12,'1133','2025-08-06','Absent',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (13,'23B81A4690','2025-08-06','Present',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (14,'23B81A4246','2025-08-06','Present',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL),
 (15,'23B81A4244','2025-08-06','Absent',NULL,NULL,NULL,NULL,NULL,'','24B81A4658',NULL);
INSERT INTO "internal_marks" ("id","student_id","subject","marks","semester","added_by") VALUES (1,'1133','M1',13,NULL,NULL),
 (2,'1133','physics',11,NULL,NULL),
 (3,'1133','Engineering Drawing',15,NULL,NULL),
 (4,'1133','BCME',12,NULL,NULL),
 (5,'1133','C language',15,NULL,NULL),
 (6,'23B81A4246','M1',13,NULL,NULL),
 (7,'23B81A4246','physics',11,NULL,NULL),
 (8,'23B81A4246','Engineering Drawing',15,NULL,NULL),
 (9,'23B81A4246','BCME',12,NULL,NULL),
 (10,'23B81A4246','C language',15,NULL,NULL);
INSERT INTO "messages" ("id","sender","receiver","message","timestamp") VALUES (1,'23B81A4246','24B81A4658','hi am mam','2025-07-21 14:58:24');
INSERT INTO "students" ("id","student_id","name","added_by","email","course","enrollment_date","username","password") VALUES (1,'1133','mani','24B81A4658','mani@gmail.com','B.Tech - Civil','2025-07-20',NULL,NULL),
 (2,'23B81A4690','venkatswamy','24B81A4658','phatannaveedali@gmail.com','B.Tech - Civil','2025-07-21',NULL,NULL),
 (4,'23B81A4246','rohith','24B81A4658','rohith@gmail.com','B.Tech - IT','2025-07-21',NULL,NULL),
 (5,'23B81A4244','rohini','24B81A4658','rohini@gmail.com','B.Tech - NAME','2025-08-06',NULL,NULL);
INSERT INTO "users" ("id","username","password","role") VALUES (1,'1122','scrypt:32768:8:1$OpPsPFqFDfZRHVIH$14794188fa69b96e155e3adb5f243fb116ed0ba809c1585e5f635a68c2dbc00c44c6848b40e00c71256ea19333cefa7e8c148b99cf24af94de12a0edab92deae','teacher'),
 (2,'24B81A4658','scrypt:32768:8:1$aBxWE3vFZLxkZNQS$4b077cd256ab45791c13c1eef05a63b42a517e84115334a603378ba4b5ee03a2b229fccecd6fa62d0305c1184f0f4743f70f6295ca1eeef96f6eb6aecd14a520','teacher'),
 (3,'23B81A4246','scrypt:32768:8:1$n4TXgh2X49jHqJiZ$85f60ea66c0ee9e4ee1171d4a099e9072779248bb0b626f00b2b5ad3b78077c0bc1e8292fba6fde7b30d95270ee605d889751ac4b722a2440afaa95cf479c8e7','student');
COMMIT;
