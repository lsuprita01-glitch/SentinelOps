
import asyncio
from datetime import datetime, timezone
from collections import defaultdict, deque

import httpx

API_URL = "http://127.0.0.1:8000"

DEMO_WINDOW_SECONDS = 60
DEMO_FAILED_LOGIN_THRESHOLD = 5

event_queue = asyncio.Queue()
login_windows = defaultdict(deque)
alerted_accounts = set()


async def generate_synthetic_events():
    print("\nSENTINELOPS REAL-TIME EVENT GENERATOR STARTED")

    event_number = 0

    while True:
        event_number += 1

        if event_number <= 6:
            event = {
                "event_id": f"EVT-{event_number:04d}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "login_failure",
                "username": "demo_admin",
                "source_ip": "192.0.2.45",
                "target": "Synthetic Authentication Server",
                "environment": "Synthetic Simulation",
                "success": False
            }
        else:
            event = {
                "event_id": f"EVT-{event_number:04d}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "login_success",
                "username": "demo_employee",
                "source_ip": "192.0.2.80",
                "target": "Synthetic Authentication Server",
                "environment": "Synthetic Simulation",
                "success": True
            }

        await event_queue.put(event)

        print(
            f"\n[NEW EVENT] {event['event_id']} | "
            f"{event['event_type']} | {event['username']}"
        )

        await asyncio.sleep(2)


def detect_suspicious_activity(event):

    if event.get("event_type") != "login_failure":
        return None

    username = event.get("username")
    source_ip = event.get("source_ip")

    if not username or not source_ip:
        return None

    now = datetime.now(timezone.utc)
    key = (username, source_ip)

    recent_events = login_windows[key]
    recent_events.append(now)

    while recent_events:
        elapsed = (now - recent_events[0]).total_seconds()

        if elapsed > DEMO_WINDOW_SECONDS:
            recent_events.popleft()
        else:
            break

    if len(recent_events) >= DEMO_FAILED_LOGIN_THRESHOLD:
        if key not in alerted_accounts:
            alerted_accounts.add(key)

            return {
                "incident_id": f"RT-{now.strftime('%Y%m%d%H%M%S')}",
                "type": "Suspicious Login Activity",
                "attack_type": "Possible Brute Force",
                "failed_attempts": len(recent_events),
                "time_window_seconds": DEMO_WINDOW_SECONDS,
                "target": "Synthetic Authentication Server",
                "username": username,
                "source_ip": source_ip,
                "unfamiliar_ip": True,
                "successful_login": False,
                "environment": "Synthetic Simulation",
                "detection_time": now.isoformat()
            }

    return None


async def send_to_api(client, endpoint, data):

    try:
        response = await client.post(
            f"{API_URL}{endpoint}",
            json=data,
            timeout=5.0
        )

        response.raise_for_status()

        print(f"[API SUCCESS] {endpoint} | HTTP {response.status_code}")

    except httpx.HTTPError as error:
        print(f"[API ERROR] {endpoint}: {error}")


async def process_events():

    print("\nSENTINELOPS EVENT PROCESSOR STARTED")

    async with httpx.AsyncClient() as client:

        while True:
            event = await event_queue.get()

            try:
                # Send every event to FastAPI
                await send_to_api(client, "/events", event)

                # Check whether the event creates a threat
                incident = detect_suspicious_activity(event)

                if incident:
                    print("\n" + "=" * 55)
                    print("SENTINELOPS: THREAT DETECTED")
                    print("=" * 55)

                    print("Incident ID:", incident["incident_id"])
                    print("Attack Type:", incident["attack_type"])
                    print("Failed Attempts:", incident["failed_attempts"])
                    print("Target:", incident["target"])
                    print("Source IP:", incident["source_ip"])

                    print("=" * 55)

                    # Send detected threat to FastAPI
                    await send_to_api(client, "/alerts", incident)

            finally:
                event_queue.task_done()


async def start_event_engine():

    print("=" * 55)
    print("SENTINELOPS CONNECTED REAL-TIME EVENT ENGINE")
    print("=" * 55)

    await asyncio.gather(
        generate_synthetic_events(),
        process_events()
    )


if __name__ == "__main__":

    try:
        asyncio.run(start_event_engine())

    except KeyboardInterrupt:
        print("\nReal-time event engine stopped.")
