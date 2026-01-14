from fastapi import FastAPI
from queue import Queue
import threading
from models import Event
from storage import init_db
from worker import worker_loop
app = FastAPI()
event_queue = Queue(maxsize=100_000)
conn = init_db()
threading.Thread(
    target=worker_loop,
    args=(event_queue, conn),
    daemon=True
).start()
@app.post("/event", status_code=202)
def ingest_event(event: Event):
    event_queue.put({
        "user_id": event.user_id,
        "timestamp": event.timestamp,
        "metadata": event.metadata
    })
    return {"status": "accepted"}
