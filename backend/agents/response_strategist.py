
import os
from dotenv import load_dotenv
from groq import Groq


def recommend_response(incident, detective_result, historical_memories, predictions):
    """
    Generates an evidence-based, advisory-only response strategy.

    Safety rules:
    - No real-world security actions are executed.
    - No unverified security thresholds are invented.
    - No account lockout policy changes are recommended.
    - All sensitive actions require human approval.
    """

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "RESPONSE STRATEGIST ERROR\n"
            "GROQ_API_KEY is missing from the .env file."
        )

    client = Groq(api_key=api_key)

    incident_id = incident.get("incident_id", "Unknown")
    failed_attempts = incident.get("failed_attempts", "Unknown")
    time_window = incident.get("time_window_minutes", "Unknown")
    target = incident.get("target", "Unknown")
    unfamiliar_ip = incident.get("unfamiliar_ip", "Unknown")
    successful_login = incident.get("successful_login", "Unknown")
    environment = incident.get("environment", "Unknown")

    source_ip = incident.get("source_ip")

    verified_facts = f"""
INCIDENT DETAILS

Incident ID: {incident_id}
Failed login attempts: {failed_attempts}
Time window: {time_window} minutes
Target: {target}
Unfamiliar IP indicator: {unfamiliar_ip}
Successful login recorded in supplied data: {successful_login}
Environment: {environment}
Exact source IP: {source_ip if source_ip else "Not provided"}

DETECTIVE FINDINGS:
{detective_result}

HISTORICAL MEMORIES:
{historical_memories}

PREDICTION REPORT:
{predictions}
"""

    system_prompt = """
You are the Response Strategist agent of SentinelOps,
an AI-powered cybersecurity incident response platform.

Your responsibility is to generate safe, evidence-based,
advisory response strategies.

STRICT SAFETY RULES:

1. Use only the supplied incident evidence.
2. Never invent IP addresses, security policies, or configurations.
3. Historical memories are references, not proof of current settings.
4. Predictions are hypotheses, not confirmed events.
5. Never recommend changing an account lockout threshold.
6. Never invent numerical security thresholds, limits, or durations.
7. Do not recommend reducing, increasing, or disabling lockout policies.
8. Recommend reviewing the existing policy with the authorized IAM team.
9. Do not recommend blocking an IP unless its exact address is available
   and its malicious nature has been verified.
10. MFA status must be checked before recommending MFA enablement.
11. Do not claim that an account is compromised unless evidence confirms it.
12. Do not execute or claim to execute any real-world action.
13. All sensitive actions require explicit human approval.
14. The environment is synthetic unless the supplied facts say otherwise.

IMPORTANT:
If a security setting is unknown, recommend collecting evidence
and verifying the existing configuration. Do not suggest changing it.

In particular, NEVER include recommendations such as:
- Reduce the account lockout threshold.
- Change the lockout duration.
- Use a threshold of 5, 10, or any other invented number.
- Configure an alert using an invented numerical threshold.

Generate the following report:

1. INCIDENT SUMMARY
2. STRATEGY A - INVESTIGATION FIRST
3. STRATEGY B - CONDITIONAL ACCOUNT PROTECTION
4. STRATEGY C - THREAT HUNTING
5. STRATEGY COMPARISON
6. RECOMMENDED APPROACH
7. MISSING INFORMATION
8. HUMAN APPROVAL

For Strategy B, include only conditional actions:
- Verify existing MFA configuration.
- Review existing account lockout policy without changing it.
- Verify the exact source IP before considering a block.
- Review account activity and monitoring.
- Consider password reset only when supported by evidence and policy.

For every action, explain the evidence needed before it can be considered.

Recommend INVESTIGATION FIRST when important evidence is missing.

End with:
HUMAN APPROVAL REQUIRED

This is an advisory simulation agent. No real-world security
configuration changes are performed.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": verified_facts
                }
            ],
            temperature=0.1,
            max_tokens=3500
        )

        report = response.choices[0].message.content or ""

        # Deterministic safety check for lockout-policy changes.
        unsafe_phrases = [
            "reduce the lockout threshold",
            "lower the lockout threshold",
            "decrease the lockout threshold",
            "reduce the lockout duration",
            "change the lockout duration",
            "disable the lockout policy",
            "short-term reduction",
            "lower the account lockout threshold"
        ]

        normalized_report = report.lower()

        detected_unsafe_advice = [
            phrase for phrase in unsafe_phrases
            if phrase in normalized_report
        ]

        if detected_unsafe_advice:
            return (
                "RESPONSE STRATEGIST SAFETY REVIEW REQUIRED\n\n"
                "The generated response contained a potentially unsafe "
                "account lockout policy recommendation.\n\n"
                "The recommendation has been withheld. Review the "
                "generated strategy and use investigation-first guidance. "
                "Do not change the existing lockout policy.\n\n"
                "HUMAN APPROVAL REQUIRED"
            )

        return (
            "\n"
            + "=" * 65
            + "\nRESPONSE STRATEGIST REPORT\n"
            + "=" * 65
            + "\n"
            + report
            + "\n\n"
            + "HUMAN APPROVAL REQUIRED\n"
            + "No real-world security actions were executed.\n"
        )

    except Exception as error:
        return (
            "RESPONSE STRATEGIST ERROR\n"
            f"Could not generate the response strategy: {error}"
        )


if __name__ == "__main__":
    print(
        "This agent is designed to run through "
        "backend.agents.orchestrator."
    )
