
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "sentinelops-security-memory"

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

if not HINDSIGHT_API_KEY or not HINDSIGHT_BASE_URL:
    raise ValueError("Check Hindsight credentials in the root .env file.")


def simulate_incident_response():

    print("\n========== SENTINELOPS SIMULATOR ==========")

    incident = {
        "incident_id": "INC-002",
        "failed_attempts": 32,
        "time_window_minutes": 2,
        "target": "privileged_employee_account",
        "successful_login": False
    }

    print("\nSIMULATED INCIDENT:")
    print(incident)

    actions = [
        {
            "name": "Temporary source IP block",
            "attempts_prevented": 20,
            "risk_reduction": 40,
            "requires_human_approval": True
        },
        {
            "name": "Enable MFA",
            "attempts_prevented": 0,
            "risk_reduction": 35,
            "requires_human_approval": True
        },
        {
            "name": "Authentication rate limiting",
            "attempts_prevented": 10,
            "risk_reduction": 25,
            "requires_human_approval": True
        }
    ]

    print("\nSIMULATING DEFENSIVE ACTIONS...")

    total_prevented = 0

    for action in actions:
        total_prevented += action["attempts_prevented"]

        print("\nAction:", action["name"])
        print("Simulated attempts prevented:",
              action["attempts_prevented"])
        print("Estimated risk reduction:",
              str(action["risk_reduction"]) + "%")
        print("Human approval required:",
              action["requires_human_approval"])

    remaining_attempts = max(
        0,
        incident["failed_attempts"] - total_prevented
    )

    outcome_score = round(
        (total_prevented / incident["failed_attempts"]) * 100,
        2
    )

    outcome = {
        "incident_id": incident["incident_id"],
        "simulation_type": "synthetic",
        "actions_simulated": [
            action["name"] for action in actions
        ],
        "remaining_attempts": remaining_attempts,
        "attempts_prevented": total_prevented,
        "outcome_score": outcome_score,
        "successful_login_confirmed": False,
        "simulation_timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }

    print("\n========== SIMULATION RESULT ==========")
    print("Attempts prevented:", total_prevented)
    print("Remaining simulated attempts:", remaining_attempts)
    print("Outcome score:", str(outcome_score) + "%")
    print("Successful login confirmed: No")

    return outcome


def store_simulation_memory(outcome):

    print("\nStoring simulation outcome in Hindsight...")

    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    try:
        memory_content = f"""
        SentinelOps synthetic simulation outcome.

        Incident ID: {outcome['incident_id']}
        Simulation type: SYNTHETIC - NOT A REAL SECURITY INCIDENT.

        Actions simulated: {', '.join(outcome['actions_simulated'])}

        Simulated attempts prevented: {outcome['attempts_prevented']}
        Remaining simulated attempts: {outcome['remaining_attempts']}
        Illustrative outcome score: {outcome['outcome_score']} percent.

        Successful login confirmed: No.

        This is an illustrative software simulation.
        It does not prove real-world control effectiveness.
        """

        result = client.retain(
            bank_id=BANK_ID,
            content=memory_content,
            context="SentinelOps synthetic simulation result",
            tags=[
                "sentinelops",
                "simulation",
                "synthetic",
                "INC-002"
            ]
        )

        print("SUCCESS: Simulation outcome sent to Hindsight.")
        print("Memory items processed:", result.items_count)

    finally:
        client.close()


if __name__ == "__main__":

    try:
        result = simulate_incident_response()
        store_simulation_memory(result)

        print("\n======================================")
        print("SENTINELOPS LEARNING CYCLE COMPLETED!")
        print("Simulation outcome stored in long-term memory.")

    except Exception as error:
        print("\nSentinelOps error:", error)
