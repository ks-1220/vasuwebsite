from flask import Blueprint, request, jsonify
import sqlite3
from backend.utils.validators import is_valid_name, is_valid_phone, is_valid_email, is_valid_message
from backend.services.email_service import send_email
import os
contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=["POST"])
def contact():
    data = request.form

    # 🛑 Honeypot spam check
    if data.get("website"):
        return jsonify({"error": "Spam detected"}), 400

    # ✅ Validation
    if not is_valid_name(data["name"]):
        return jsonify({"error": "Invalid name"}), 400

    if not is_valid_phone(data["phone"]):
        return jsonify({"error": "Invalid phone"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email"}), 400

    if not is_valid_message(data["message"]):
        return jsonify({"error": "Message too short"}), 400

    # 💾 Save to database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "database", "inquiries.db")
   )

    print("DB PATH:", DB_PATH)
    print("Exists:", os.path.exists(DB_PATH))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO inquiries (name, phone, email, query, message)
    VALUES (?, ?, ?, ?, ?)
""", (
    data["name"],
    data["phone"],
    data["email"],
    data["query"],
    data["message"]
))

    conn.commit()
    conn.close()


    # 📧 Send email
    send_email(data)
    return jsonify({"status": "success", "message": "Inquiry submitted"})
