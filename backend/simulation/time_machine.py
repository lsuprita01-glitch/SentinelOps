
import os

from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

BANK_ID = "sentinelops-security-memory"
GROQ_MODEL = "openai/gpt-oss-120b"


# ==========================================
# SENTINELOPS - CYBERATTACK TIME MACHINE
# ==========================================

INCIDENT_HISTORY = [
    {
        "incident_id": "INC-001",
        "title": "Employee Authentication Brute Force",
        "attack_type": "Brute Force",
        "failed_attempts": 45,
        "time_window_minutes": 3,
        "target": "Employee Authentication Server",
        "severity": "High",
        "environment": "Synthetic Simulation"
    },
    {
        "incident_id": "INC-002",
        "title": "Repeated Privileged Account Login Failures",
        "attack_type": "Suspicious Login Activity",
        "failed_attempts": 32,
        "time_window_minutes": 2,
        "target": "Privileged Employee Account",
        "severity": "High",
        "environment": "Synthetic Simulation"
    }
]


# ==========================================
# 1. CONNECT TO HINDSIGHT
# ==========================================

def connect_hindsight():

    api_key = os.getenv("HINDSIGHT_API_KEY")
    base_url = os.getenv("HINDSIGHT_BASE_URL")

    if not api_key or not base_url:
        raise ValueError(
            "Hindsight credentials are missing from .env"
        )

    return Hindsight(
        base_url=base_url,
        api_key=api_key
    )


# ==========================================
# 2. CONNECT TO GROQ
# ==========================================

def connect_groq():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key is missing from .env"
        )

    return Groq(api_key=api_key)


# ==========================================
# 3. DISPLAY INCIDENT HISTORY
# ==========================================

def list_incidents():

    print("\n========== CYBERATTACK TIME MACHINE ==========")

    print("\nAVAILABLE HISTORICAL INCIDENTS:\n")

    for incident in INCIDENT_HISTORY:

        print("----------------------------------------")
        print("Incident ID:", incident["incident_id"])
        print("Title:", incident["title"])
        print("Attack Type:", incident["attack_type"])
        print("Failed Attempts:", incident["failed_attempts"])
        print("Severity:", incident["severity"])
        print("Environment:", incident["environment"])

    print("----------------------------------------")


# ==========================================
# 4. RETRIEVE HINDSIGHT MEMORIES
# ==========================================

def retrieve_hindsight_memories(incident):

    print("\n========== HINDSIGHT MEMORY RETRIEVAL ==========")

    print("Connecting to SentinelOps memory bank...")

    client = connect_hindsight()

    query = (
        f"{incident['attack_type']} "
        f"{incident['failed_attempts']} failed login attempts "
        f"in {incident['time_window_minutes']} minutes. "
        f"Target: {incident['target']}. "
        "Retrieve relevant historical incidents, defensive actions, "
        "outcomes and lessons learned."
    )

    try:

        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        memories = []

        for item in result.results[:5]:
            memories.append(item.text)

        if memories:

            print("\nACTUAL HINDSIGHT MEMORIES:\n")

            for index, memory in enumerate(memories, start=1):
                print(f"\nMEMORY {index}:")
                print(memory)

        else:

            print("\nNo matching memories were found.")

        return memories

    finally:

        client.close()


# ==========================================
# 5. REPLAY INCIDENT
# ==========================================

def replay_incident(incident):

    print("\n========== INCIDENT REPLAY ==========")

    print("Incident:", incident["incident_id"])
    print("Title:", incident["title"])

    timeline = [
        "Suspicious authentication activity detected.",
        (
            f"{incident['failed_attempts']} failed attempts "
            f"reported within {incident['time_window_minutes']} minutes."
        ),
        "Detective Agent investigates available evidence.",
        "Memory Agent retrieves historical experience.",
        "Prediction Agent evaluates possible next stages.",
        "Response Strategist prepares defensive recommendations.",
        "Auditor checks evidence and approval requirements."
    ]

    print("\nATTACK TIMELINE:\n")

    for index, event in enumerate(timeline):
        print(f"[T+00:{index:02d}] {event}")


# ==========================================
# 6. GENERATE AI RESPONSE
# ==========================================

def generate_ai_response(
    client,
    incident,
    memories=None
):

    current_facts = f"""
Incident ID: {incident['incident_id']}
Incident type: {incident['attack_type']}
Failed attempts: {incident['failed_attempts']}
Time window: {incident['time_window_minutes']} minutes
Target: {incident['target']}
Severity: {incident['severity']}
Environment: {incident['environment']}
"""

    if memories is None:

        memory_context = """
NO HISTORICAL MEMORY IS AVAILABLE.

Analyse the incident using only the current incident facts.
Do not invent previous incidents or outcomes.
"""

        mode = "WITHOUT HISTORICAL MEMORY"

    else:

        memory_context = "\n".join(
            f"- {memory}" for memory in memories
        )

        if not memory_context:
            memory_context = "No relevant historical memories found."

        mode = "WITH HINDSIGHT MEMORY"

    prompt = f"""
You are SentinelOps, an AI cybersecurity incident response assistant.

Analyse the following synthetic security incident.

CURRENT INCIDENT FACTS:
{current_facts}

MEMORY MODE:
{mode}

HISTORICAL MEMORY CONTEXT:
{memory_context}

INSTRUCTIONS:

1. Separate confirmed incident facts from assumptions.
2. If historical memory is available, explain how it is relevant.
3. Never treat historical actions as proof of current security settings.
4. Do not invent MFA status, source IP addresses, successful logins,
   attacker identity, malware, or compromise.
5. Recommend investigation steps before security configuration changes.
6. Clearly identify actions requiring human approval.
7. Do not execute any real security action.
8. Explain what the available memory contributes to the analysis.
9. If no relevant memory exists, explicitly say so.

Return your response under these headings:

INCIDENT ANALYSIS
AVAILABLE EVIDENCE
HISTORICAL MEMORY INFLUENCE
DEFENSIVE RECOMMENDATIONS
MISSING INFORMATION
HUMAN APPROVAL REQUIREMENTS
LESSONS FOR FUTURE INCIDENTS
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful cybersecurity analyst. "
                    "Use evidence-based reasoning and never invent facts."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=1600
    )

    return response.choices[0].message.content or ""


# ==========================================
# 7. COMPARE AI RESPONSES
# ==========================================

def compare_ai_responses(
    incident,
    memories
):

    print("\n========== AI LEARNING COMPARISON ==========")

    client = connect_groq()

    try:

        # First analysis: no historical memory

        print("\n[1/2] ANALYSING WITHOUT HISTORICAL MEMORY...")

        without_memory = generate_ai_response(
            client,
            incident,
            memories=None
        )

        print("\n========== WITHOUT MEMORY ==========\n")
        print(without_memory)

        # Second analysis: with Hindsight memories

        print("\n[2/2] ANALYSING WITH HINDSIGHT MEMORY...")

        with_memory = generate_ai_response(
            client,
            incident,
            memories=memories
        )

        print("\n========== WITH HINDSIGHT MEMORY ==========\n")
        print(with_memory)

        # Final comparison

        print("\n========== LEARNING COMPARISON SUMMARY ==========")

        print("\nWITHOUT MEMORY:")
        print(
            "The AI analysed the incident using only "
            "the supplied current facts."
        )

        print("\nWITH MEMORY:")
        print(
            "The AI received current facts and relevant "
            "historical Hindsight experiences."
        )

        print("\nMEMORY RESULTS:")
        print("Retrieved memories:", len(memories))

        print("\nIMPORTANT:")
        print(
            "Different recommendations do not automatically "
            "prove improved accuracy or security performance."
        )

        print(
            "This comparison demonstrates the influence of "
            "historical context, not a measured learning score."
        )

        return {
            "without_memory": without_memory,
            "with_memory": with_memory
        }

    finally:

        client.close()


# ==========================================
# 8. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    list_incidents()

    selected_id = input(
        "\nEnter incident ID to replay (INC-001 / INC-002): "
    ).strip().upper()

    selected_incident = next(
        (
            item for item in INCIDENT_HISTORY
            if item["incident_id"] == selected_id
        ),
        None
    )

    if selected_incident is None:

        print("\nInvalid incident ID.")
        raise SystemExit(1)

    # Retrieve actual historical memories

    memories = retrieve_hindsight_memories(
        selected_incident
    )

    # Replay incident

    replay_incident(
        selected_incident
    )

    # Compare AI responses

    comparison = compare_ai_responses(
        selected_incident,
        memories
    )

    print("\n========================================")
    print("CYBERATTACK TIME MACHINE COMPLETED")
    print("========================================")
