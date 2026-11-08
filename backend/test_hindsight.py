
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")
base_url = os.getenv("HINDSIGHT_BASE_URL")

if not api_key or not base_url:
    raise ValueError("Check Hindsight credentials in .env")

client = Hindsight(
    base_url=base_url,
    api_key=api_key
)

try:
    bank = client.create_bank(
        bank_id="sentinelops-security-memory",
        name="SentinelOps Security Memory",
        reflect_mission=(
            "You are the long-term memory system for SentinelOps. "
            "Remember verified cybersecurity incidents, evidence, "
            "response actions and their outcomes. Always distinguish "
            "confirmed facts from unverified predictions."
        )
    )

    print("SUCCESS! Hindsight is connected.")
    print("Memory bank:", bank.bank_id)

except Exception as error:
    print("Connection failed:", error)

finally:
    client.close()
