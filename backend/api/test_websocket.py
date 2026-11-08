
import asyncio
import websockets
import json


async def test_connection():

    uri = "ws://127.0.0.1:8000/ws/events"

    print("Connecting to SentinelOps WebSocket...")

    async with websockets.connect(uri) as websocket:

        print("CONNECTED SUCCESSFULLY!")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            print("\nLIVE MESSAGE RECEIVED:")
            print(json.dumps(data, indent=4))


if __name__ == "__main__":
    asyncio.run(test_connection())

