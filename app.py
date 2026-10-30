"""
Digital Notice Board System
Flask Web Application for College & Campus Announcements
"""

import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, abort
)
import database

app = Flask(__name__)
# Secret key for session signing
app.secret_key = os.environ.get("SECRET_KEY", "college-digital-notice-board-secret-key-2026")

# Valid notice categories and priorities
ALLOWED_CATEGORIES = [
    "All", "Academic", "Examination", "Events",
    "Placement", "Sports", "General"
]
FORM_CATEGORIES = [
    "Academic", "Examination", "Events",
    "Placement", "Sports", "General"
]
ALLOWED_PRIORITIES = ["Normal", "Important", "Urgent"]


def login_required(f):
    """Decorator to protect admin routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" not in session or not session.get("admin_logged_in"):
            flash("Please sign in to access the administrator panel.", "warning")
            return redirect(url_for("admin_login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.template_filter("format_date")
def format_date_filter(date_str):
    """Custom Jinja filter to display human-readable formatted timestamps."""
    if not date_str:
        return ""
    try:
        # Handles 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD'
        if " " in str(date_str):
            dt = datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%b %d, %Y • %I:%M %p")
        else:
            dt = datetime.strptime(str(date_str), "%Y-%m-%d")
            return dt.strftime("%b %d, %Y")
    except Exception:
        return str(date_str)


@app.before_request
def ensure_db_initialized():
    """Ensure database tables exist before handling any request."""
    # We run init once when app context initializes
    if not hasattr(app, "_db_initialized"):
        database.init_db()
        app._db_initialized = True


# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.route("/")
def index():
    """Public Notice Board view with category filters, keyword search, and sorting."""
    selected_category = request.args.get("category", "All")
    search_query = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "date_desc")

    # Fetch notices matching criteria
    notices = database.get_all_notices(
        category=selected_category,
        search=search_query,
        sort_by=sort_by
    )

    stats = database.get_statistics()

    return render_template(
        "index.html",
        notices=notices,
        categories=ALLOWED_CATEGORIES,
        selected_category=selected_category,
        search_query=search_query,
        sort_by=sort_by,
        stats=stats
    )


@app.route("/notice/<int:notice_id>")
def notice_detail(notice_id):
    """Individual notice detail view with incremented view count and printable format."""
    notice = database.get_notice_by_id(notice_id, increment_view=True)
    if not notice:
        flash("The requested notice was not found.", "danger")
        return redirect(url_for("index"))

    return render_template("notice_detail.html", notice=notice)


@app.route("/api/notice/<int:notice_id>")
def api_notice_detail(notice_id):
    """JSON API endpoint to quickly load notice details in client-side modal."""
    notice = database.get_notice_by_id(notice_id, increment_view=True)
    if not notice:
        return jsonify({"success": False, "message": "Notice not found"}), 404

    return jsonify({
        "success": True,
        "notice": {
            "id": notice["id"],
            "title": notice["title"],
            "category": notice["category"],
            "content": notice["content"],
            "posted_by": notice["posted_by"],
            "priority": notice["priority"],
            "is_pinned": bool(notice["is_pinned"]),
            "views_count": notice["views_count"],
            "expiry_date": notice["expiry_date"],
            "created_at": notice["created_at"]
        }
    })


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def admin_login():
    """Admin login page with authentication and input validation."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please provide both username and password.", "warning")
            return render_template("admin_login.html", username=username)

        admin = database.authenticate_admin(username, password)
        if admin:
            session["admin_logged_in"] = True
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            session["admin_name"] = admin["full_name"]
            session["admin_role"] = admin["role"]

            flash(f"Welcome back, {admin['full_name']}! You have signed in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin_dashboard"))
        else:
            flash("Invalid administrator credentials. Please verify your username and password.", "danger")
            return render_template("admin_login.html", username=username)

    return render_template("admin_login.html")


@app.route("/logout")
def admin_logout():
    """Sign out the current administrator."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("index"))


# ==========================================
# ADMIN MANAGEMENT ROUTES
# ==========================================

@app.route("/admin")
@login_required
def admin_dashboard():
    """Admin dashboard overview and list of all notices with management controls."""
    selected_category = request.args.get("category", "All")
    search_query = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "date_desc")

    notices = database.get_all_notices(
        category=selected_category,
        search=search_query,
        sort_by=sort_by
    )
    stats = database.get_statistics()

    return render_template(
        "admin_dashboard.html",
        notices=notices,
        categories=ALLOWED_CATEGORIES,
        selected_category=selected_category,
        search_query=search_query,
        sort_by=sort_by,
        stats=stats
    )


@app.route("/admin/notice/new", methods=["GET", "POST"])
@login_required
def notice_create():
    """Create a new campus notice with comprehensive validation."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        priority = request.form.get("priority", "Normal").strip()
        posted_by = request.form.get("posted_by", "").strip()
        expiry_date = request.form.get("expiry_date", "").strip()
        content = request.form.get("content", "").strip()
        is_pinned = 1 if request.form.get("is_pinned") else 0

        # Form validations
        errors = []
        if not title or len(title) < 5:
            errors.append("Notice title must be at least 5 characters long.")
        if len(title) > 200:
            errors.append("Notice title cannot exceed 200 characters.")
        if category not in FORM_CATEGORIES:
            errors.append("Please select a valid notice category.")
        if priority not in ALLOWED_PRIORITIES:
            errors.append("Please select a valid priority level.")
        if not posted_by or len(posted_by) < 2:
            errors.append("Please specify the issuing department or authority.")
        if not content or len(content) < 10:
            errors.append("Notice content must be at least 10 characters long.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "notice_form.html",
                action="create",
                categories=FORM_CATEGORIES,
                priorities=ALLOWED_PRIORITIES,
                form_data=request.form
            )

        try:
            new_id = database.create_notice(
                title=title,
                category=category,
                content=content,
                posted_by=posted_by,
                priority=priority,
                is_pinned=is_pinned,
                expiry_date=expiry_date or None
            )
            flash(f"Notice #{new_id} published successfully!", "success")
            return redirect(url_for("admin_dashboard"))
        except Exception as e:
            flash(f"Database error while saving notice: {str(e)}", "danger")

    return render_template(
        "notice_form.html",
        action="create",
        categories=FORM_CATEGORIES,
        priorities=ALLOWED_PRIORITIES,
        form_data={}
    )


@app.route("/admin/notice/edit/<int:notice_id>", methods=["GET", "POST"])
@login_required
def notice_edit(notice_id):
    """Edit an existing notice."""
    notice = database.get_notice_by_id(notice_id)
    if not notice:
        flash("Notice not found.", "danger")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        priority = request.form.get("priority", "Normal").strip()
        posted_by = request.form.get("posted_by", "").strip()
        expiry_date = request.form.get("expiry_date", "").strip()
        content = request.form.get("content", "").strip()
        is_pinned = 1 if request.form.get("is_pinned") else 0

        errors = []
        if not title or len(title) < 5:
            errors.append("Notice title must be at least 5 characters long.")
        if category not in FORM_CATEGORIES:
            errors.append("Please select a valid category.")
        if priority not in ALLOWED_PRIORITIES:
            errors.append("Please select a valid priority.")
        if not posted_by or len(posted_by) < 2:
            errors.append("Please specify the issuing authority.")
        if not content or len(content) < 10:
            errors.append("Notice content must be at least 10 characters long.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "notice_form.html",
                action="edit",
                notice=notice,
                categories=FORM_CATEGORIES,
                priorities=ALLOWED_PRIORITIES,
                form_data=request.form
            )

        try:
            database.update_notice(
                notice_id=notice_id,
                title=title,
                category=category,
                content=content,
                posted_by=posted_by,
                priority=priority,
                is_pinned=is_pinned,
                expiry_date=expiry_date or None
            )
            flash("Notice updated successfully!", "success")
            return redirect(url_for("admin_dashboard"))
        except Exception as e:
            flash(f"Failed to update notice: {str(e)}", "danger")

    return render_template(
        "notice_form.html",
        action="edit",
        notice=notice,
        categories=FORM_CATEGORIES,
        priorities=ALLOWED_PRIORITIES,
        form_data=notice
    )


@app.route("/admin/notice/delete/<int:notice_id>", methods=["POST"])
@login_required
def notice_delete(notice_id):
    """Delete a notice."""
    notice = database.get_notice_by_id(notice_id)
    if not notice:
        flash("Notice not found.", "warning")
    else:
        database.delete_notice(notice_id)
        flash(f"Notice '{notice['title'][:40]}...' has been deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/notice/toggle-pin/<int:notice_id>", methods=["POST"])
@login_required
def notice_toggle_pin(notice_id):
    """Toggle sticky/pinned status for a notice."""
    database.toggle_pin_notice(notice_id)
    flash("Notice pin status updated.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reset-data", methods=["POST"])
@login_required
def reset_sample_data():
    """Reset notice board data back to the default sample dataset."""
    database.seed_sample_notices()
    flash("Notice board has been successfully reloaded with default sample data!", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    # Ensure database is initialized before starting development server
    database.init_db()
    # Runs locally on port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
