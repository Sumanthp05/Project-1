
## Architecture Diagram (Textual)

Client → POST /event (202) → FastAPI (Producer) → enqueue (non-blocking) → In-Memory Queue → batch consume → Background Worker → executemany() → SQLite


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

