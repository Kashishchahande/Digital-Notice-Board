"""
Database management and operations for Digital Notice Board System.
Uses Python's built-in sqlite3 module with lightweight helper functions.
"""

import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notice_board.db")


def get_db_connection():
    """Establish and return a connection to the SQLite database with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and create default admin and sample notices if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Admins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'Administrator',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Notices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            posted_by TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Normal',
            is_pinned INTEGER DEFAULT 0,
            views_count INTEGER DEFAULT 0,
            expiry_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Seed default admin if none exists
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        default_password = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO admins (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, ("admin", default_password, "System Administrator", "Dean of Academic Affairs"))
        conn.commit()

    # Seed sample notices if empty
    cursor.execute("SELECT COUNT(*) FROM notices")
    if cursor.fetchone()[0] == 0:
        seed_sample_notices(conn)

    conn.close()


def seed_sample_notices(conn=None):
    """Seed comprehensive realistic college notices for demonstration."""
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    cursor = conn.cursor()

    # Delete existing notices before seeding fresh sample data
    cursor.execute("DELETE FROM notices")

    sample_notices = [
        (
            "Mid-Semester Examination Schedule - Fall Semester 2026",
            "Examination",
            "The Mid-Semester Examinations for all Undergraduate and Postgraduate courses will commence from November 15, 2026. Detailed department-wise timetables and seating plans have been published on the student portal. Students must carry their valid identity cards and hall tickets to the examination hall. Use of smartwatches and electronic devices is strictly prohibited.",
            "Controller of Examinations",
            "Urgent",
            1,
            142,
            "2026-11-25",
            "2026-10-28 09:30:00"
        ),
        (
            "Campus Placement Drive: CloudTech & Global Systems Registration",
            "Placement",
            "Eligible Final Year students (B.Tech CSE, IT, ECE with CGPA 7.0 and above) are invited to register for the upcoming joint campus placement drive by CloudTech Innovations and Global Systems. CTC offered ranges from 7.5 LPA to 14 LPA. The online aptitude and coding assessment will take place on November 8, 2026. Register via the placement portal before November 4, 2026, 5:00 PM.",
            "Training & Placement Cell",
            "Urgent",
            1,
            285,
            "2026-11-05",
            "2026-10-29 11:15:00"
        ),
        (
            "Annual Technical Symposium & Hackathon 'Innovate 2026'",
            "Events",
            "Department of Computer Science & Engineering presents the 12th Annual National Technical Symposium 'Innovate 2026' on November 20-21, 2026. Events include a 24-Hour Hackathon, Paper Presentation, Web Design Sprint, and Robo-Wars. Total cash prizes worth Rs. 1,50,000 to be won. Teams can register at the symposium portal. Early bird registration ends November 10.",
            "CSE Department Coordinator",
            "Important",
            0,
            198,
            "2026-11-22",
            "2026-10-27 14:00:00"
        ),
        (
            "Submission Deadline for Final Year Capstone Project Abstract",
            "Academic",
            "All final year students must submit their finalized Capstone Project title, team member details, and abstract signed by their project guide to the respective department academic committee on or before November 12, 2026. Late submissions will result in a deduction of internal evaluation marks. No team modifications will be entertained after this date.",
            "Academic Affairs Committee",
            "Important",
            0,
            164,
            "2026-11-13",
            "2026-10-26 10:00:00"
        ),
        (
            "Inter-Department Football & Badminton Championship 2026",
            "Sports",
            "The Annual Inter-Department Sports Tournament 2026 will be held at the University Sports Complex from November 18 to November 24, 2026. Interested students should submit team rosters to the Physical Education Director before November 10. Selection trials for the college varsity team will also be conducted during these matches.",
            "Director of Physical Education",
            "Normal",
            0,
            89,
            "2026-11-25",
            "2026-10-25 16:45:00"
        ),
        (
            "Extended Central Library Hours During Exam Preparation",
            "Academic",
            "In view of the approaching examinations, the Central Library reading halls will remain open 24/7 starting from November 1, 2026, until the conclusion of semester exams. Digital library terminals and Wi-Fi facilities will be operational throughout this period. Please maintain silence and follow library protocol.",
            "Chief Librarian",
            "Normal",
            0,
            120,
            "2026-12-15",
            "2026-10-24 13:20:00"
        ),
        (
            "National Holiday Announcement: Campus Closed on November 5",
            "General",
            "All students, faculty members, and administrative staff are hereby notified that the college campus and administrative offices will remain closed on November 5, 2026, on account of the state public holiday. Regular academic classes and lab sessions will resume on November 6, 2026, as per regular schedule.",
            "Principal & Registrar Office",
            "Normal",
            0,
            310,
            "2026-11-06",
            "2026-10-23 15:30:00"
        ),
        (
            "Expert Guest Lecture on Generative AI & Deep Learning Architectures",
            "Academic",
            "A technical masterclass on 'Generative AI & Transformer Models in Industry' is scheduled on Saturday, November 7, 2026, at 11:00 AM in the Main Auditorium. The session will be delivered by Dr. R. K. Sharma, Senior AI Research Scientist. All 3rd and 4th year students are strongly encouraged to attend. E-certificates will be provided to registered attendees.",
            "Dean of Research & Innovation",
            "Important",
            0,
            215,
            "2026-11-08",
            "2026-10-22 09:00:00"
        )
    ]

    cursor.executemany("""
        INSERT INTO notices (
            title, category, content, posted_by, priority,
            is_pinned, views_count, expiry_date, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [(n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8], n[8]) for n in sample_notices])

    conn.commit()
    if should_close:
        conn.close()


def get_all_notices(category=None, search=None, sort_by="date_desc"):
    """Fetch notices with optional category filtering, keyword search, and sorting."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM notices WHERE 1=1"
    params = []

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query += " AND (title LIKE ? OR content LIKE ? OR posted_by LIKE ?)"
        params.extend([search_term, search_term, search_term])

    # Pinned notices always appear on top, followed by user selected sorting
    if sort_by == "date_asc":
        query += " ORDER BY is_pinned DESC, created_at ASC"
    elif sort_by == "priority":
        # Order: Urgent, Important, Normal
        query += """ ORDER BY is_pinned DESC, 
                     CASE priority 
                         WHEN 'Urgent' THEN 1 
                         WHEN 'Important' THEN 2 
                         WHEN 'Normal' THEN 3 
                         ELSE 4 
                     END, created_at DESC"""
    elif sort_by == "views":
        query += " ORDER BY is_pinned DESC, views_count DESC, created_at DESC"
    else:  # default: date_desc (newest first)
        query += " ORDER BY is_pinned DESC, created_at DESC"

    cursor.execute(query, params)
    notices = cursor.fetchall()
    conn.close()
    return notices


def get_notice_by_id(notice_id, increment_view=False):
    """Fetch a single notice by ID and optionally increment its view counter."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if increment_view:
        cursor.execute("UPDATE notices SET views_count = views_count + 1 WHERE id = ?", (notice_id,))
        conn.commit()

    cursor.execute("SELECT * FROM notices WHERE id = ?", (notice_id,))
    notice = cursor.fetchone()
    conn.close()
    return notice


def create_notice(title, category, content, posted_by, priority="Normal", is_pinned=0, expiry_date=None):
    """Insert a new notice into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notices (title, category, content, posted_by, priority, is_pinned, expiry_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (title.strip(), category.strip(), content.strip(), posted_by.strip(), priority, int(is_pinned), expiry_date or None))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_notice(notice_id, title, category, content, posted_by, priority="Normal", is_pinned=0, expiry_date=None):
    """Update an existing notice."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE notices
        SET title = ?, category = ?, content = ?, posted_by = ?, priority = ?, is_pinned = ?, expiry_date = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title.strip(), category.strip(), content.strip(), posted_by.strip(), priority, int(is_pinned), expiry_date or None, notice_id))
    conn.commit()
    conn.close()


def delete_notice(notice_id):
    """Delete a notice by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
    conn.commit()
    conn.close()


def toggle_pin_notice(notice_id):
    """Toggle the pinned state of a notice."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_pinned FROM notices WHERE id = ?", (notice_id,))
    row = cursor.fetchone()
    if row:
        new_state = 0 if row["is_pinned"] == 1 else 1
        cursor.execute("UPDATE notices SET is_pinned = ? WHERE id = ?", (new_state, notice_id))
        conn.commit()
    conn.close()


def get_statistics():
    """Retrieve statistical summary for dashboard and header."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notices")
    total_notices = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notices WHERE is_pinned = 1")
    pinned_notices = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notices WHERE priority = 'Urgent'")
    urgent_notices = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT category) FROM notices")
    total_categories = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(views_count), 0) FROM notices")
    total_views = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) as count FROM notices GROUP BY category ORDER BY count DESC")
    category_breakdown = cursor.fetchall()

    conn.close()

    return {
        "total_notices": total_notices,
        "pinned_notices": pinned_notices,
        "urgent_notices": urgent_notices,
        "total_categories": total_categories,
        "total_views": total_views,
        "category_breakdown": category_breakdown
    }


def authenticate_admin(username, password):
    """Verify administrator credentials."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ?", (username.strip(),))
    admin = cursor.fetchone()
    conn.close()

    if admin and check_password_hash(admin["password_hash"], password):
        return {
            "id": admin["id"],
            "username": admin["username"],
            "full_name": admin["full_name"],
            "role": admin["role"]
        }
    return None
