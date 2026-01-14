import asyncio
import aiohttp

URL = "http://127.0.0.1:8000/event"

async def send_event(session, i):
    async with session.post(
        URL,
        json={
            "user_id": i,
            "timestamp": "2025-01-01T00:00:00Z",
            "metadata": {"test": True}
        }
    ) as resp:
        print("Status:", resp.status)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_event(session, i) for i in range(1000)]
        await asyncio.gather(*tasks)

    print("Load test finished")

if __name__ == "__main__":
    asyncio.run(main())
