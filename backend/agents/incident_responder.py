
import os
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

BANK_ID = "sentinelops-security-memory"

if not all([GROQ_API_KEY, HINDSIGHT_API_KEY, HINDSIGHT_BASE_URL]):
    raise ValueError("Check API credentials in the root .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)

memory_client = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)


def investigate_incident():

    incident = """
    Incident ID: INC-002
    Type: Suspicious login activity
    Environment: Simulated authentication server

    Evidence:
    - 32 failed login attempts within 2 minutes.
    - Attempts targeted a privileged employee account.
    - One attempt originated from an unfamiliar simulated IP.
    - No successful login has been confirmed.

    Severity: High
    Status: Under investigation.
    """

    print("\n========== SENTINELOPS ==========")
    print("\nNEW SECURITY INCIDENT:")
    print(incident)

    print("\nSearching Hindsight long-term memory...")

    memory_result = memory_client.recall(
        bank_id=BANK_ID,
        query=(
            "Find previous simulated brute-force or suspicious "
            "login incidents, their evidence, defensive actions "
            "and outcomes."
        )
    )

    memories = []

    if memory_result.results:
        for item in memory_result.results:
            memories.append(item.text)

    memory_context = (
        "\n".join(memories)
        if memories
        else "No relevant historical incidents were found."
    )

    print("\nHISTORICAL MEMORY:")
    print(memory_context)

    print("\nConsulting SentinelOps AI...")

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
                You are SentinelOps, a defensive cybersecurity
                incident response assistant.

                Separate confirmed evidence, historical facts
                and hypotheses.

                Never invent missing evidence.
                Never claim an attack succeeded without proof.
                Recommend defensive actions only.
                Do not execute actions on real systems.
                Require human approval for disruptive actions.
                Explain how historical memory influenced decisions.
                """
            },
            {
                "role": "user",
                "content": f"""
                NEW INCIDENT:
                {incident}

                HISTORICAL MEMORY:
                {memory_context}

                Provide:
                1. Incident classification and severity.
                2. Confirmed evidence.
                3. Relevant historical lessons.
                4. Possible next attack stages (hypotheses).
                5. Three defensive recommendations.
                6. How memory influenced the recommendations.
                7. What a human analyst must verify.

                Do not assume that missing details are facts.
                """
            }
        ],
        temperature=0.2,
        max_completion_tokens=1200
    )

    print("\n========== AI INVESTIGATION ==========\n")
    print(response.choices[0].message.content)

    print("\nSUCCESS: SentinelOps investigation completed!")
    print("Historical memory and AI analysis connected.")
    print("Recommendations are advisory only.")


if __name__ == "__main__":
    try:
        investigate_incident()
    except Exception as error:
        print("\nSentinelOps error:", error)
    finally:
        memory_client.close()
        groq_client.close()
