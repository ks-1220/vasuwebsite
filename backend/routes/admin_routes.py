from flask import Blueprint, render_template, request, redirect, session
import sqlite3
import os

admin_bp = Blueprint("admin", __name__)

# ---------- DB PATH (SAFE & ABSOLUTE) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "database", "inquiries.db")
)

# ---------- ADMIN CREDENTIALS ----------
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Safety check
        if not ADMIN_USERNAME or not ADMIN_PASSWORD:
            return "Admin credentials not set", 500

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect("/admin/dashboard")

        return "Invalid credentials", 401

    return render_template("login.html")


@admin_bp.route("/admin/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM inquiries ORDER BY id DESC")
    inquiries = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", inquiries=inquiries)


@admin_bp.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin")
