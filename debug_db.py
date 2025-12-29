
import sqlite3
import os
import sys

# Adjust path to import backend modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.database import get_db_connection, init_db, DB_PATH

print(f"Checking database at: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("[MISSING] Database file does NOT exist.")
else:
    print("[OK] Database file exists.")

print("Attempting to initialize DB (create table if missing)...")
try:
    init_db()
except Exception as e:
    print(f"[ERROR] init_db failed: {e}")

print("Attempting test insertion...")
try:
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check schema
    cur.execute("PRAGMA table_info(inquiries)")
    columns = cur.fetchall()
    if not columns:
        print("[MISSING] Table 'inquiries' does NOT exist.")
    else:
        print("[OK] Table 'inquiries' exists. Columns:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")

    # Try Insert
    cur.execute("""
        INSERT INTO inquiries (name, phone, email, query, message)
        VALUES (?, ?, ?, ?, ?)
    """, ("TestUser", "1234567890", "test@example.com", "Test Query", "Test Message"))
    conn.commit()
    print("[SUCCESS] Test insertion SUCCESS.")
    conn.close()

except Exception as e:
    print(f"[FAILED] Test insertion FAILED: {e}")
