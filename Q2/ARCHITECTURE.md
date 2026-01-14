
## Architecture Diagram (Textual)

Client
  |
  | POST /event (HTTP 202)
  v
FastAPI Application (Producer)
  |
  | enqueue (non-blocking)
  v
In-Memory Queue (Python Queue)
  |
  | batch consumption
  v
Background Worker Thread (Consumer)
  |
  | executemany() batch insert
  v
SQLite Database

---

## Buffering Strategy
An in-memory queue is used to temporarily store incoming events.
This decouples request handling from database writes.

Events are flushed to the database when:
- The batch size threshold is reached, OR
- A time-based flush interval expires

---

## Persistence Strategy
- SQLite is used as the SQL database (treated as PostgreSQL for design purposes)
- Metadata is serialized to JSON and stored safely using parameterized queries

---

## Resilience
If the database is temporarily unavailable (simulated via an exclusive lock),
the API continues accepting requests and buffering data in memory.
Once the database recovers, buffered events are written successfully.

---

## Design Rationale
- Non-blocking API ensures high throughput
- Batch inserts improve performance
- Clear separation between API and storage layers

