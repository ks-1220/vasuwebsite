import sqlite3

conn = sqlite3.connect(
    r"C:\Users\ASUS\Desktop\vasu\backend\database\inquiries.db"
)
cur = conn.cursor()

cur.execute("ALTER TABLE inquiries ADD COLUMN query TEXT;")

conn.commit()
conn.close()
