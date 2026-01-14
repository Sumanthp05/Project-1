Objective:
Build a thread-safe inventory system that prevents overselling and underselling under high concurrent load.

Stock: 100 units

Traffic: 50–1000 concurrent purchase requests

Core Challenge:
Prevent race conditions when multiple clients attempt to decrement the same inventory record simultaneously.

Concurrency Strategy

Database-enforced atomic update

UPDATE inventory
SET stock = stock - 1
WHERE item_id = 1 AND stock > 0;


Check and decrement occur atomically

Guarantees no negative inventory

Safe across threads and processes

Equivalent to row-level locking (SELECT FOR UPDATE)

API Behavior

POST /buy_ticket

200 OK → purchase successful

410 GONE → stock exhausted

No application-level locks

No deadlocks by design

Rollback on unexpected DB errors

Safe failure semantics under contention

Proof of Correctness

proof_of_correctness.py:

Spawns ≥ 200 concurrent threads

Verifies:
Exactly 100 purchases recorded
Final stock = 0
No overselling or underselling

Scalability:
Works under multi-threaded and multi-process deployments
Proof script can be scaled to 1,000 concurrent requests without code changes