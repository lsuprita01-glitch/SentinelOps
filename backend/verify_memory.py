
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

try:
    print("\n========== SENTINELOPS MEMORY TEST ==========")

    result = client.recall(
        bank_id="sentinelops-security-memory",
        query=(
            "Recall the latest SentinelOps synthetic simulation "
            "for incident INC-002. What defensive actions were "
            "simulated, how many attempts were prevented, "
            "and what was the outcome score?"
        )
    )

    if result.results:
        print("\nSUCCESS: Hindsight recalled stored information!")

        for item in result.results:
            print("\nRECALLED MEMORY:")
            print(item.text)

    else:
        print("\nNo matching memory found.")

finally:
    client.close()
