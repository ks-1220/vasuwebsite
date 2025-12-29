from flask import Blueprint, request, jsonify
from backend.utils.validators import is_valid_name, is_valid_phone, is_valid_email, is_valid_message
from backend.services.email_service import send_email
from backend.database import get_db_connection
import sys

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
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO inquiries (name, phone, email, query, message)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["phone"],
            data["email"],
            data.get("query", "General"), # Handle missing query field gracefully
            data["message"]
        ))

        conn.commit()
        conn.close()
        print("✅ Inquiry saved to database successfully.")
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        # DEBUG: Return actual error to user to see what's wrong
        return jsonify({"error": f"Database error details: {str(e)}"}), 500

    # 📧 Send email (Non-blocking failure)
    email_status = "sent"
    try:
        send_email(data)
        print("✅ Email notification sent.")
    except Exception as e:
        # Log the error but DO NOT fail the request
        print(f"⚠️ Email Warning: {e}")
        email_status = f"failed: {str(e)}"
        
        # We return 200 because the PRIMARY goal (saving to DB) was successful.
        # The user said "ye errors nhi ana chahiye" (should not get these errors).
    
    return jsonify({
        "status": "success", 
        "message": "Inquiry submitted successfully!",
        "email_debug": email_status # Optional: for debugging
    }), 200
