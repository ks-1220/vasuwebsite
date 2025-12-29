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
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        DB_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "database", "inquiries.db")
       )

        print("DB PATH:", DB_PATH)
        # Note: On Vercel, this will likely fail if the DB is not in a writable location (read-only FS)
        # For now, we wrap it to ensure email still sends.
        
        # Check if directory exists, if not trying to create it will fail on read-only
        # So we just try to connect if file exists
        
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
    except Exception as e:
        print(f"Warning: Database write failed (likely Read-Only FS on Vercel): {e}")
        # Continue to send email even if DB fails


    # 📧 Send email
    try:
        send_email(data)
        return jsonify({"status": "success", "message": "Inquiry submitted"})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": f"Email failed: {str(e)}"}), 500
