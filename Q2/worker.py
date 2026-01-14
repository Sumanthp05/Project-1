import time
from queue import Queue, Empty
from storage import insert_batch
BATCH_SIZE = 100
FLUSH_INTERVAL = 1.0  # seconds
# def worker_loop(queue: Queue, conn):
#     buffer = []
#     last_flush = time.time()
#     while True:
#         try:
#             event = queue.get(timeout=0.1)
#             buffer.append(event)
#         except Empty:
#             pass
#         now = time.time()
#         if len(buffer) >= BATCH_SIZE or (buffer and now - last_flush >= FLUSH_INTERVAL):
#             try:
#                 insert_batch(conn, buffer)
#                 buffer.clear()
#                 last_flush = now
#             except Exception:
#                 # DB down → retry later
#                 time.sleep(1)
def worker_loop(queue: Queue, conn):
    buffer = []
    last_flush = time.time()

    print("Worker started")

    while True:
        try:
            event = queue.get(timeout=0.1)
            buffer.append(event)
        except Empty:
            pass

        now = time.time()
        if buffer and (len(buffer) >= BATCH_SIZE or now - last_flush >= FLUSH_INTERVAL):
            # print(f"Flushing batch of size: {len(buffer)}")

            try:
                insert_batch(conn, buffer)
                buffer.clear()
                last_flush = now
            except Exception:
                time.sleep(1)
