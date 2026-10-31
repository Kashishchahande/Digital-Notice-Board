# Digital Notice Board System

A modern, responsive, Python and Flask-based web application designed for colleges, universities, and educational institutions to publish, organize, and view academic announcements, examination schedules, placement notices, and campus events.

---

## 1. Description

The **Digital Notice Board System** replaces traditional paper bulletin boards with a centralized, real-time electronic notice portal. Students, faculty members, and visitors can instantly browse announcements filtered by category (Academic, Examination, Events, Placement, Sports, General) or sorted by date, importance, or views.

Administrators have access to a secure, password-protected portal where they can publish notices, pin urgent announcements to the top of the board, edit existing records, and manage expiration dates.

---

## 2. Problem Statement

In colleges and universities, physical notice boards suffer from numerous drawbacks:
- **Clutter & Disorganization:** Overlapping paper notices get lost, damaged, or torn down.
- **Delayed Information Flow:** Commuter students and remote learners miss time-sensitive updates such as sudden room changes, exam postponement, or deadline shifts.
- **Paper & Resource Waste:** Printing dozens of circulars daily wastes paper and administrative effort.
- **No Search or Categorization:** Students waste time scanning bulletin boards to find placement notices or department-specific circulars.

**Solution:** The Digital Notice Board System digitizes campus communications into a 24/7 accessible web application featuring real-time categorization, keyword searching, priority badges, and one-click printable official notices.

---

## 3. Key Features

### For Students and Public Users:
- **Category Filtering:** Filter announcements by Academic, Examination, Events, Placement, Sports, or General.
- **Date & Priority Sorting:** Sort notices by Newest First, Oldest First, Priority (Urgent first), or Most Viewed.
- **Instant Keyword Search:** Real-time search across notice titles, content bodies, and issuing departments.
- **Pinned / Sticky Notices:** Urgent circulars and critical notices stay pinned at the top with a distinct gold badge.
- **Urgent Alert Indicators:** High-priority notices feature a pulsing crimson badge for immediate visual prominence.
- **Quick Modal Preview:** Read full notice text instantly in an interactive overlay without full page reloads.
- **Dedicated Notice Page & Share Link:** Share direct links to individual circulars with reference IDs.
- **Clean Print View:** Built-in `@media print` CSS formats notices as official white-paper circulars with institutional stamps for physical printing or saving as PDF.
- **Live Campus Clock & Statistics:** Real-time date/clock header and summary counters (Total Notices, Urgent Alerts, Pinned Announcements, Total Reads).

### For Administrators:
- **Secure Authentication:** Session-based authentication with Werkzeug password hashing.
- **Notice Management Console:** Central dashboard with tabular overview, status flags, and quick action buttons.
- **Create & Edit Notices:** Rich form with real-time live preview that updates as the administrator types.
- **Pin / Unpin Toggle:** Instant one-click toggle to make any notice sticky.
- **Expiration Dates:** Optional expiry date handling to flag out-of-date notices.
- **Demo Mode / Data Reset:** One-click "Reset Sample Data" button to restore a clean set of realistic college sample notices at any time during project viva demonstrations.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.x | Core programming language |
| **Web Framework** | Flask 3.x | Routing, request lifecycle, session handling, view rendering |
| **Database** | SQLite3 | Embedded SQL database for persistent storage (zero configuration) |
| **Password Security** | Werkzeug Security | PBKDF2:SHA256 password hashing for administrator accounts |
| **Templating Engine** | Jinja2 | Dynamic HTML rendering with custom filters |
| **Frontend** | HTML5, CSS3, Vanilla JS | Modern UI without bulky external JavaScript dependencies |
| **Typography** | Plus Jakarta Sans & JetBrains Mono | Modern typography |
| **Production WSGI** | Gunicorn | High-concurrency production HTTP WSGI server for cloud deployment |
| **Deployment** | Render / Any cloud host | Compatible with `Procfile` and `render.yaml` |

---

## 5. Project Structure

```
digital-notice-board/
├── app.py                     # Main Flask application (routes, validation, sessions)
├── database.py                # Database connection, SQLite schema, queries & sample data
├── requirements.txt           # Python dependencies (Flask, Werkzeug, gunicorn)
├── Procfile                   # Process file for Render / Heroku deployment
├── render.yaml                # Render cloud deployment configuration
├── .gitignore                 # Excludes caches, virtual environments, and local DB
├── README.md                  # Complete documentation & viva preparation
├── test_app.py                # Automated unit and integration test suite
├── templates/
│   ├── base.html              # Base layout with navbar, alerts, live clock & modal
│   ├── index.html             # Public notice board (cards, search, categories, sort)
│   ├── notice_detail.html     # Single notice official circular view & print layout
│   ├── admin_login.html       # Administrator sign-in with 1-click demo fill
│   ├── admin_dashboard.html   # Admin management table with metrics and controls
│   └── notice_form.html       # Add/Edit form with real-time live preview panel
└── static/
    ├── css/
    │   └── style.css          # Responsive dark-accented modern styles + print stylesheet
    └── js/
        └── main.js            # Live clock, modal fetch, share clipboard, mobile menu
```

---

## 6. Installation & Local Setup

### Prerequisites
- Python 3.8 or higher installed on your computer.
- `pip` package manager.
- Git (optional, for version control).

### Step 1: Clone or Navigate to the Project
```bash
cd "d:\Python report"
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
On Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```
On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Web Browser
Navigate to:
```
http://127.0.0.1:5000
```

> **Default Administrator Credentials:**
> - **Username:** `admin`
> - **Password:** `admin123`
> *(A "One-Click Fill Demo Credentials" button is provided on the login page for effortless viva demonstration).*

---

## 7. How It Works (System Workflow)

```
[ User Request ]
       │
       ▼
┌─────────────────────────┐
│     Flask Router        │  app.py
└────────────┬────────────┘
             │
   ┌─────────┴─────────┐
   ▼                   ▼
[ Public Board ]   [ Admin Portal ]
 - Filter Category  - Login / Session Check
 - Search Keyword   - Add / Edit Notice Form
 - Sort by Date     - Delete / Pin Notice
 - View Counter     - Reset Sample Data
   │                   │
   └─────────┬─────────┘
             ▼
┌─────────────────────────┐
│   Database Controller   │  database.py (SQLite3)
│   - notices table       │
│   - admins table        │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  Jinja2 Templates & UI  │  HTML5 + Modern CSS + Vanilla JS
│  - Responsive Cards     │
│  - Modal Quick Preview  │
│  - Official Print View  │
└─────────────────────────┘
```

---

## 8. Database Schema Design

The application utilizes an SQLite database (`notice_board.db`) containing two relational tables:

### 1. `notices` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique reference identifier |
| `title` | TEXT | NOT NULL | Headline of the notice (5–200 chars) |
| `category` | TEXT | NOT NULL | Academic, Examination, Events, Placement, Sports, General |
| `content` | TEXT | NOT NULL | Complete notice body text |
| `posted_by` | TEXT | NOT NULL | Issuing authority/department |
| `priority` | TEXT | DEFAULT 'Normal' | Normal, Important, Urgent |
| `is_pinned` | INTEGER | DEFAULT 0 | 1 = Sticky/Pinned at top, 0 = Regular |
| `views_count`| INTEGER | DEFAULT 0 | Cumulative number of times viewed |
| `expiry_date`| TEXT | NULLABLE | Validity date (YYYY-MM-DD) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Publication timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last modified timestamp |

### 2. `admins` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Administrator ID |
| `username` | TEXT | UNIQUE NOT NULL | Unique login username |
| `password_hash` | TEXT | NOT NULL | Secure salted PBKDF2:SHA256 password hash |
| `full_name` | TEXT | NOT NULL | Display name (e.g., System Administrator) |
| `role` | TEXT | DEFAULT 'Administrator' | Role title |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |

---

## 9. Core Algorithms & Logic

### 1. Dynamic Notice Filtering & Prioritized Sorting
When the user accesses the board, notices are fetched using a parameterized dynamic SQL query:
```sql
SELECT * FROM notices 
WHERE 1=1 
  AND (:category = 'All' OR category = :category)
  AND (:search IS NULL OR title LIKE :search OR content LIKE :search OR posted_by LIKE :search)
ORDER BY is_pinned DESC, 
  CASE :sort_by
    WHEN 'priority' THEN 
      CASE priority WHEN 'Urgent' THEN 1 WHEN 'Important' THEN 2 ELSE 3 END
    WHEN 'date_asc' THEN created_at ASC
    WHEN 'views' THEN views_count DESC
    ELSE created_at DESC
  END;
```
- **Pinned First Rule:** Notice records with `is_pinned = 1` always precede non-pinned records regardless of the active sort order.
- **SQL Injection Prevention:** All queries use SQLite parameter bindings (`?`) rather than string concatenation.

### 2. Password Hashing Algorithm
Admin security uses `werkzeug.security`:
- Registration / Seeding: `generate_password_hash("admin123", method="pbkdf2:sha256")`
- Verification: `check_password_hash(stored_hash, submitted_password)`
Passwords are never stored in plaintext.

### 3. Asynchronous Modal Data Fetching
When the user clicks "Quick Preview" on a notice card:
1. JavaScript invokes `fetch('/api/notice/' + id)` without a full page reload.
2. The server increments `views_count` in the database and returns JSON.
3. The DOM elements of the modal are populated dynamically, and the modal dialog is displayed.

---

## 10. Sample Input & Output

### Sample Input (Admin Creating Notice):
- **Title:** `Mid-Semester Examination Schedule - Fall Semester 2026`
- **Category:** `Examination`
- **Priority:** `Urgent`
- **Issuing Department:** `Controller of Examinations`
- **Expiry Date:** `2026-11-25`
- **Pin to Top:** `Checked (True)`
- **Content:** `The Mid-Semester Examinations for all Undergraduate and Postgraduate courses will commence from November 15, 2026. Students must carry valid hall tickets.`

### Sample Output:
- **Notice Card on Board:** Displayed at the very top of the grid with a gold `PINNED ANNOUNCEMENT` ribbon, an amber `Examination` pill, and a red pulsing `Urgent` indicator badge.
- **Search Result:** Searching "Mid-Semester" or "Examinations" immediately isolates this notice.
- **Printed Document:** Clicking "Print Notice" generates an institutional circular format:
  ```
  OFFICIAL CAMPUS CIRCULAR                REF: NTC-2026-0001
  Mid-Semester Examination Schedule - Fall Semester 2026
  Category: Examination | Priority: Urgent | Date: Oct 28, 2026
  -------------------------------------------------------------
  The Mid-Semester Examinations for all Undergraduate...
  -------------------------------------------------------------
  Issued By: Controller of Examinations
  [ OFFICIAL VERIFIED BULLETIN ]
  ```

---

## 11. Automated Testing

The project includes an automated test suite in `test_app.py` covering:
- Database initialization and admin credential verification
- Category filtering and search query parsing
- Sorting by date, priority, and view counts
- JSON API endpoint response integrity
- Protected admin routes and authentication redirects
- Form input validation (title length, content length, valid categories)
- Notice creation, editing, pin toggling, and deletion

Run tests with:
```bash
python test_app.py
```
Expected output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in ~1.2s

OK
```

---

## 12. Viva Preparation & Frequently Asked Questions

### High-Level Summary for Viva
> "The Digital Notice Board System is a lightweight, responsive web application built with Python and Flask. It provides a centralized communication hub where college administrators can post, edit, pin, and categorize official announcements, and students can view, search, and sort notices in real-time. It uses an SQLite database for persistent storage, Werkzeug for secure password hashing, and pure CSS/JS for a modern, responsive user experience."

---

### Top 10 Viva Questions and Answers

#### Q1: What problem does this project solve?
**Answer:** It replaces traditional, messy physical bulletin boards with an organized, 24/7 web-accessible notice board. Students can filter notices by department or date, search by keyword, and view urgent alerts immediately from any device.

#### Q2: Why did you choose Flask instead of Django for this project?
**Answer:** Flask is a lightweight micro-framework that is easy to understand, provides complete control over routing and database logic, and does not carry the bulky overhead of Django. It is ideal for focused college mini projects.

#### Q3: Which database is used and why?
**Answer:** SQLite3. It is serverless, zero-configuration, comes built into Python's standard library, and stores all data in a single file (`notice_board.db`). It provides full ACID-compliant SQL support without needing an external database server like MySQL or PostgreSQL.

#### Q4: How is security handled for the administrator panel?
**Answer:**
1. Administrator passwords are encrypted using PBKDF2:SHA256 password hashing.
2. Route protection is implemented using a custom `@login_required` decorator that verifies active Flask sessions.
3. SQL injection is prevented by using parameterized SQLite queries (`?` placeholders).

#### Q5: How do pinned (sticky) notices work?
**Answer:** Each notice record has an integer column `is_pinned` (1 or 0). The database query uses `ORDER BY is_pinned DESC, created_at DESC`, ensuring all pinned notices appear at the top of the feed regardless of other sorting criteria.

#### Q6: How does the "Quick Preview" modal work without reloading the page?
**Answer:** When the user clicks "Quick Preview", JavaScript makes an asynchronous `fetch()` call to the Flask endpoint `/api/notice/<id>`. The server returns the notice data as JSON, and JavaScript populates the modal DOM elements and displays the overlay.

#### Q7: How does the application handle responsive design on mobile phones?
**Answer:** We use modern CSS3 flexbox and CSS grid layouts with media queries at breakpoints (1024px, 768px, and 480px). On mobile devices, the multi-column card grid collapses into a single stacked column, tables enable smooth horizontal scrolling, and navigation collapses into a touch-friendly hamburger menu.

#### Q8: How is the print functionality implemented?
**Answer:** Using CSS `@media print` rules. When the user triggers print or PDF export, non-essential web elements (navbar, buttons, footer, and dark backgrounds) are hidden, and the notice is rendered as a clean, black-and-white formal institutional circular.

#### Q9: What happens if an administrator submits an empty or invalid form?
**Answer:** Server-side validation checks that the title is at least 5 characters long, the content is at least 10 characters long, and the category belongs to the allowed list. If validation fails, user-friendly flash messages are displayed and the entered data is preserved.

#### Q10: How do you deploy this project to production?
**Answer:** The project is configured with a `Procfile` (`web: gunicorn app:app`) and `render.yaml`. On production servers (such as Render), Gunicorn runs as a production WSGI server that manages worker processes to handle concurrent requests.

---

## 13. Future Scope

1. **Email / SMS Broadcasts:** Automatically email or SMS urgent notices to subscribed students.
2. **File & PDF Attachments:** Allow administrators to attach PDF timetables, syllabus circulars, or brochures.
3. **Role-Based Access Control (RBAC):** Separate department logins so the Placement Officer can only publish placement notices.
4. **Push Notifications:** Web push notifications for instant urgent alerts on Android and desktop devices.
5. **Notice Archival Automation:** A background cron job that automatically archives notices past their expiry date.

---

## 14. Deployment to Render

This repository is ready for 1-click deployment on [Render](https://render.com):
1. Push this repository to GitHub.
2. Log in to Render and click **New > Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy Web Service**.

---

## 15. Repository & Live Application Links

- **GitHub Repository:** *To be linked upon remote push*
- **Live Application:** *To be linked upon cloud deployment*
- **Author:** Shamique Ansari
- **License:** Open-source for educational use.

#   K a s h i s h _ V S _ C o d e _ R e p o  
 