import threading
import requests
import sqlite3

URL = "http://127.0.0.1:5000/buy_ticket"
SUCCESS = 0
FAIL = 0

lock = threading.Lock()


def attempt_purchase():
    global SUCCESS, FAIL
    response = requests.post(URL)

    with lock:
        if response.status_code == 200:
            SUCCESS += 1
        else:
            FAIL += 1


threads = []

for _ in range(50):
    t = threading.Thread(target=attempt_purchase)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Successful purchases:", SUCCESS)
print("Failed purchases:", FAIL)

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("SELECT stock FROM inventory WHERE item_id = 1;")
stock = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM purchases;")
purchases = cursor.fetchone()[0]

conn.close()

print("Final stock:", stock)
print("Total purchase records:", purchases)
