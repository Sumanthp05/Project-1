import sqlite3
import time
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

DB_PATH = "ledger.db"

# Thread pool for background transaction processing
executor = ThreadPoolExecutor(max_workers=5)


# -----------------------------
# Database Utilities
# -----------------------------

def get_db_connection():
    """
    Creates a new SQLite connection.
    Each thread must have its own connection.
    """
    return sqlite3.connect(DB_PATH, isolation_level=None)


# -----------------------------
# Search Endpoint (SECURE)
# -----------------------------

@app.route("/search", methods=["GET"])
def search_users():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username = ?",
            (query,)
        )
        rows = cursor.fetchall()

        results = [
            {"id": r[0], "username": r[1], "role": r[2]}
            for r in rows
        ]

        return jsonify(results)

    finally:
        conn.close()


# -----------------------------
# Background Transaction Logic
# -----------------------------

def process_transaction_background(user_id: int, amount: float):
    """
    Runs in a background thread.
    Simulates slow banking core and performs
    atomic balance update.
    """
    # Simulate slow external dependency
    time.sleep(3)

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Explicit transaction
        cursor.execute("BEGIN")

        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE id = ?",
            (amount, user_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("User not found")

        cursor.execute("COMMIT")

    except Exception:
        cursor.execute("ROLLBACK")
        raise

    finally:
        conn.close()


# -----------------------------
# Transaction Endpoint (NON-BLOCKING)
# -----------------------------

@app.route("/transaction", methods=["POST"])
def process_transaction():
    data = request.json or {}

    user_id = data.get("user_id")
    amount = data.get("amount")

    if user_id is None or amount is None:
        return jsonify({"error": "Missing user_id or amount"}), 400

    try:
        user_id = int(user_id)
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid user_id or amount"}), 400

    # Submit background task
    executor.submit(process_transaction_background, user_id, amount)

    # Immediate response keeps API responsive
    return jsonify({"status": "Transaction processing started"}), 202


if __name__ == "__main__":
    app.run(debug=False)
