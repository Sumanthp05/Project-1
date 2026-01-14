from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/buy_ticket", methods=["POST"])
def buy_ticket():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE inventory
            SET stock = stock - 1
            WHERE item_id = 1 AND stock > 0;
        """)

        if cursor.rowcount == 0:
            conn.commit()
            return jsonify({"error": "Sold out"}), 410

        cursor.execute(
            "INSERT INTO purchases (item_id) VALUES (1);"
        )

        conn.commit()
        return jsonify({"message": "Purchase successful"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Internal error"}), 500

    finally:
        conn.close()


if __name__ == "__main__":
    app.run(threaded=True)
