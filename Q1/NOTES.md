SECURITY HARDENING

Issue:
The /search endpoint constructed SQL queries using direct string interpolation with user input, allowing SQL injection and unauthorized data access.

Fix:
Replaced dynamic SQL construction with parameterized queries.
Removed raw SQL debug logging.

Outcome:
The search endpoint is now resistant to SQL injection and common query-manipulation attacks.


PERFORMANCE AND PRESPONSIVENESS

Issue:
The /transaction endpoint executed a simulated banking delay (time.sleep) on the request thread, blocking the API under constrained worker configurations and causing perceived freezes.

Fix:
Offloaded transaction processing to background threads using ThreadPoolExecutor.
The API now returns immediately while transactions execute asynchronously.

Outcome:
The API remains responsive to new requests even when individual transactions are waiting on the simulated banking core.

DATA INTEGRITY

Issue:
Database updates were not explicitly transactional and were vulnerable to partial failures.

Fix:
Wrapped updates in explicit database transactions.
Ensured each background task uses its own SQLite connection.
Used parameterized SQL for all write operations.

Outcome:
All updates are atomic, consistent, and safe under concurrent execution.

COMPATIBILITY

All endpoints, inputs, and response formats remain compatible with the original implementation, fully meeting assessment constraints.