import sqlite3
import time

conn = sqlite3.connect("events.db")
cur = conn.cursor()

print("Locking database for 5 seconds...")
cur.execute("BEGIN EXCLUSIVE")
time.sleep(5)

conn.commit()
conn.close()
print("Database lock released")
