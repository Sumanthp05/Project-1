import sqlite3

DB_PATH = "inventory.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    item_id INTEGER PRIMARY KEY,
    stock INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Reset state (important for re-runs)
cursor.execute("DELETE FROM inventory;")
cursor.execute("DELETE FROM purchases;")

cursor.execute(
    "INSERT INTO inventory (item_id, stock) VALUES (1, 100);"
)

conn.commit()
conn.close()

print("Database initialized with stock = 100")
