
import os
import stat
import sqlite3

# Valid path: root/database/inquiries.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "inquiries.db")

print(f"Fixing permissions for: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("[MISSING] Database file does NOT exist. Initializing directly...")
    # Try to initialize it if missing
    try:
        if not os.path.exists(os.path.dirname(DB_PATH)):
            os.makedirs(os.path.dirname(DB_PATH))
        conn = sqlite3.connect(DB_PATH)
        conn.close()
        print("[CREATED] Empty database file created.")
    except Exception as e:
        print(f"[ERROR] Could not create file: {e}")
        exit(1)

# 1. Check and fix file permissions
try:
    current_perms = os.stat(DB_PATH).st_mode
    print(f"Current permissions: {oct(current_perms)}")

    # Add Write permission
    os.chmod(DB_PATH, stat.S_IWRITE | stat.S_IREAD)
    print("[OK] Forced Write permissions on file.")
except Exception as e:
    print(f"[ERROR] Failed to chmod: {e}")

# 2. Enable Write-Ahead Logging (WAL)
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    mode = cur.fetchone()
    print(f"[OK] Journal Mode set to: {mode[0]}")
    conn.commit()
    conn.close()
except Exception as e:
    print(f"[ERROR] Failed to set WAL mode (file locked?): {e}")

if "OneDrive" in DB_PATH:
    print("\n[WARNING] Project is inside OneDrive.")
    print("OneDrive 'locks' database files. If this persists, pause OneDrive sync or move the project.")

