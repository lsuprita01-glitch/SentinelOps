
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = "sentinelops-security-memory"

try:
    # Store a simulated cybersecurity incident
    incident = """
    SIMULATED SECURITY INCIDENT - INC-001

    Attack type: Brute-force login attempt
    Target asset: Employee authentication server
    Evidence: 45 failed login attempts within 3 minutes.
    Source: Synthetic test logs.
    Severity: High.

    Response: The simulated security team blocked the
    suspicious source IP and enabled multi-factor
    authentication for the affected account.

    Outcome: Further unauthorized login attempts
    were prevented in this simulation.

    Lesson: Repeated failed logins should trigger
    investigation, account protection and monitoring.
    This is synthetic training data, not a real incident.
    """

    print("Storing simulated incident...")

    stored = client.retain(
        bank_id=BANK_ID,
        content=incident,
        context="SentinelOps simulated cybersecurity incident",
        tags=["simulation", "brute-force", "INC-001"]
    )

    print("Memory stored!")
    print("Items processed:", stored.items_count)

    # Retrieve the stored memory
    print("\nSearching SentinelOps memory...")

    result = client.recall(
        bank_id=BANK_ID,
        query="What happened in the previous brute-force attack and what response worked?"
    )

    if result.results:
        print("\nRECALLED MEMORIES:")
        for memory in result.results:
            print("-", memory.text)
    else:
        print("No memories returned yet. Try again shortly.")

except Exception as error:
    print("Error:", error)

finally:
    client.close()
