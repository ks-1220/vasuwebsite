from flask import Blueprint, render_template, request, redirect, session
from backend.database import get_db_connection
import os

admin_bp = Blueprint("admin", __name__)

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

    # Use centralized connection
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inquiries ORDER BY id DESC")
    inquiries = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", inquiries=inquiries)


@admin_bp.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin")
