
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "sentinelops-security-memory"


def recall_incidents(query):

    print("\n========== MEMORY AGENT ==========")
    print("Searching SentinelOps long-term memory...")

    api_key = os.getenv("HINDSIGHT_API_KEY")
    base_url = os.getenv("HINDSIGHT_BASE_URL")

    if not api_key or not base_url:
        raise ValueError("Hindsight credentials are missing.")

    client = Hindsight(
        base_url=base_url,
        api_key=api_key
    )

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        memories = []

        if result.results:
            for item in result.results[:5]:
                memories.append(item.text)

        if memories:
            print("\nRELEVANT HISTORICAL MEMORIES:")

            for memory in memories:
                print("-", memory)
        else:
            print("No relevant historical memories found.")

        print("\nMemory retrieval completed.")

        return memories

    finally:
        client.close()
