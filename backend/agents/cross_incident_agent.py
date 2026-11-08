
import os
import re
import unicodedata

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "sentinelops-security-memory"
GROQ_MODEL = "openai/gpt-oss-120b"


# ==================================================
# 1. CONNECTIONS
# ==================================================

def connect_hindsight():

    api_key = os.getenv("HINDSIGHT_API_KEY")
    base_url = os.getenv("HINDSIGHT_BASE_URL")

    if not api_key or not base_url:
        raise ValueError("Hindsight credentials missing from .env")

    return Hindsight(
        base_url=base_url,
        api_key=api_key
    )


def connect_groq():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing from .env")

    return Groq(api_key=api_key)


# ==================================================
# 2. INCIDENT VALIDATION
# ==================================================

def validate_incident(incident):

    required_fields = [
        "incident_id",
        "type",
        "failed_attempts",
        "time_window_minutes",
        "target",
        "unfamiliar_ip",
        "successful_login",
        "environment"
    ]

    missing = [
        field for field in required_fields
        if field not in incident
    ]

    if missing:
        raise ValueError(f"Missing incident fields: {missing}")

    if not isinstance(incident["failed_attempts"], int):
        raise ValueError("failed_attempts must be an integer")

    if incident["failed_attempts"] < 0:
        raise ValueError("failed_attempts cannot be negative")

    if incident["time_window_minutes"] <= 0:
        raise ValueError("time_window_minutes must be positive")

    if not isinstance(incident["unfamiliar_ip"], bool):
        raise ValueError("unfamiliar_ip must be Boolean")

    if not isinstance(incident["successful_login"], bool):
        raise ValueError("successful_login must be Boolean")


# ==================================================
# 3. HINDSIGHT MEMORY RETRIEVAL
# ==================================================

def retrieve_related_incidents(incident):

    client = connect_hindsight()

    query = (
        f"Previous cybersecurity incidents related to "
        f"{incident['type']}, failed authentication attempts, "
        f"brute-force patterns, employee accounts, "
        f"defensive actions and verified outcomes."
    )

    try:

        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        memories = []

        if result and result.results:

            for item in result.results[:10]:

                memory_text = getattr(item, "text", None)

                if memory_text:
                    memories.append(memory_text)

        return memories

    finally:

        close_method = getattr(client, "close", None)

        if callable(close_method):
            close_method()


# ==================================================
# 4. TEXT NORMALIZATION
# ==================================================

def normalize_text(text):

    text = unicodedata.normalize("NFKC", str(text))

    for character in [
        "\u2010", "\u2011", "\u2012",
        "\u2013", "\u2014", "\u2212"
    ]:
        text = text.replace(character, "-")

    return text.lower()


def clean_heading(line):

    line = normalize_text(line).strip()

    line = re.sub(r"^[\s#>*`]+", "", line)
    line = re.sub(r"[\s*`]+$", "", line)

    return line.strip()


# ==================================================
# 5. REPORT SECTION EXTRACTION
# ==================================================

def extract_section(report, section_number, next_section_number):

    lines = report.splitlines()

    collecting = False
    collected = []

    for line in lines:

        heading = clean_heading(line)

        current_pattern = (
            rf"^{section_number}\s*[\.\):]\s*"
        )

        next_pattern = (
            rf"^{next_section_number}\s*[\.\):]\s*"
        )

        if re.match(current_pattern, heading):

            collecting = True
            continue

        if collecting and re.match(next_pattern, heading):
            break

        if collecting:
            collected.append(line)

    return "\n".join(collected).strip()


# ==================================================
# 6. CROSS-INCIDENT AI ANALYSIS
# ==================================================

def analyse_incident_relationships(incident, memories):

    groq = connect_groq()

    current_facts = f"""
CURRENT INCIDENT - VERIFIED INPUT DATA

Incident ID: {incident['incident_id']}
Incident type: {incident['type']}
Failed attempts: {incident['failed_attempts']}
Time window: {incident['time_window_minutes']} minutes
Target: {incident['target']}
Unfamiliar IP indicator: {incident['unfamiliar_ip']}
Successful login recorded in supplied data: {incident['successful_login']}
Environment: {incident['environment']}

Exact source IP supplied: {bool(incident.get('source_ip'))}
"""

    historical_memories = (
        "\n".join(f"- {memory}" for memory in memories)
        if memories
        else "No historical memories were retrieved."
    )

    prompt = f"""
You are the Cross-Incident Intelligence Agent of SentinelOps.

Your responsibility is to compare a current cybersecurity incident
with historical experiences retrieved from Hindsight.

{current_facts}

HISTORICAL MEMORY DATA:

{historical_memories}


IMPORTANT EVIDENCE RULES:

1. Current incident facts must come only from the supplied
   current incident fields.

2. Historical information must remain clearly labelled
   as historical information.

3. Never combine current and historical facts into one
   unverified statement.

4. Similar failed-login counts do not prove the same attacker.

5. Similar time windows do not prove shared infrastructure.

6. A privileged employee account is NOT automatically
   the same asset as an employee authentication server.

7. An unfamiliar IP indicator does not provide an exact IP address.

8. A historical blocked IP does not prove that the current
   incident uses the same IP.

9. Do not invent usernames, hostnames, IP addresses,
   devices, domains or asset identifiers.

10. If no exact technical indicator matches, explicitly state:
    "No verified shared indicators found."

11. Do not claim that two incidents are connected merely
    because they have similar behaviour.

12. A successful_login value of False means no successful
    login is recorded in the supplied current incident data.
    Do not claim that all systems have been checked.

13. Do not invent security configurations or security policies.

14. Historical simulated results do not prove real-world
    effectiveness of a security control.

15. Every prediction must be labelled as a hypothesis.

16. Recommendations must start with investigation and verification.

17. Do not recommend changing MFA, lockout settings,
    rate limits or other controls without checking their
    current configuration and obtaining human approval.

18. Do not recommend IP blocking without an exact verified IP.

19. Do not invent numerical thresholds or confidence percentages.

20. If the evidence is insufficient, clearly say so.


USE THESE EXACT NUMBERED HEADINGS:

1. CURRENT INCIDENT SUMMARY

Include only supplied current incident facts.

2. HISTORICAL INCIDENTS RETRIEVED

Summarize relevant memories. Remember that multiple memory
fragments may describe the same historical incident.

3. EVIDENCE-BACKED SIMILARITIES

Describe behavioural similarities separately from
technical indicators.

Do not claim a shared server, account or attacker without evidence.

4. SHARED TECHNICAL INDICATORS

List exact verified matching indicators only.

If none exist, write:
"No verified shared indicators found."

5. HISTORICAL RESPONSE AND OUTCOME

Describe recorded historical actions and their outcomes.
Do not claim that they guarantee success in the current incident.

6. INTELLIGENCE GAPS

List information needed for stronger correlation.

7. RELATIONSHIP CONFIDENCE

Choose LOW, MEDIUM or HIGH.

Explain the evidence supporting the choice.
Use LOW when only general behavioural similarities exist.

8. RECOMMENDATIONS

Prioritize log collection, evidence verification,
account monitoring and investigation.

Before proposing a security configuration change,
require verification of its current state and human approval.

9. CONCLUSION

Explain what historical memory contributes and
what cannot be established from the available evidence.


End the report with this exact statement:

HUMAN APPROVAL REQUIRED: All sensitive response actions must be
reviewed and approved by an authorized human analyst before execution.
"""

    response = groq.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict evidence-based cybersecurity "
                    "analyst. You must distinguish facts, historical "
                    "memories, similarities and hypotheses. Never "
                    "invent technical evidence."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1,
        max_completion_tokens=2000
    )

    return response.choices[0].message.content.strip()


# ==================================================
# 7. DETERMINISTIC SAFETY AUDIT
# ==================================================

def audit_report(incident, report):

    issues = []
    review_items = []

    normalized = normalize_text(report)

    similarities = extract_section(report, 3, 4)
    shared = extract_section(report, 4, 5)
    recommendations = extract_section(report, 8, 9)

    normalized_shared = normalize_text(shared)
    normalized_recommendations = normalize_text(recommendations)

    # CHECK 1: Required headings

    required_headings = [
        "current incident summary",
        "historical incidents retrieved",
        "evidence-backed similarities",
        "shared technical indicators",
        "historical response and outcome",
        "intelligence gaps",
        "relationship confidence",
        "recommendations",
        "conclusion"
    ]

    for heading in required_headings:

        if heading not in normalized:
            issues.append(f"Missing report heading: {heading}")

    # CHECK 2: Evidence sections must exist

    if not similarities.strip():
        issues.append("Evidence-backed similarities section is empty.")

    if not shared.strip():
        issues.append("Shared technical indicators section is empty.")

    # CHECK 3: Shared indicator accuracy

    behavioral_terms = [
        "failed attempts",
        "failed login attempts",
        "time window",
        "login attempts",
        "minutes"
    ]

    if (
        "no verified shared indicators found" not in normalized_shared
        and any(
            term in normalized_shared
            for term in behavioral_terms
        )
    ):

        review_items.append(
            "Review whether behavioural similarities "
            "have been incorrectly labelled as shared indicators."
        )

    # CHECK 4: Unsupported successful-login claims

    if incident["successful_login"] is False:

        risky_claims = [
            "attacker successfully logged in",
            "attacker gained access",
            "password was exposed",
            "credentials were stolen"
        ]

        for claim in risky_claims:

            if claim in normalized:
                issues.append(
                    f"Potential unsupported claim: {claim}"
                )

    # CHECK 5: Unsupported server and account connections

    unsupported_connections = [
        "both incidents targeted the same server",
        "both incidents used the same account",
        "the same attacker conducted both attacks",
        "the same ip address was used",
        "both incidents involved the same hostname"
    ]

    for claim in unsupported_connections:

        if claim in normalized:
            issues.append(
                f"Unsupported relationship claim: {claim}"
            )

    # CHECK 6: IP blocking without an exact IP

    if not incident.get("source_ip"):

        blocking_patterns = [
            r"\bblock\s+(?:the\s+)?(?:unfamiliar\s+)?ip\b",
            r"\bblock\s+(?:the\s+)?source\s+ip\b",
            r"\bblock\s+(?:the\s+)?subnet\b",
            r"\bblock\s+(?:the\s+)?network\s+range\b",
            r"\bdeny\s+(?:the\s+)?ip\b"
        ]

        for pattern in blocking_patterns:

            if re.search(pattern, normalized_recommendations):

                issues.append(
                    "IP blocking recommended without an exact "
                    "verified source IP."
                )

                break

    # CHECK 7: Numerical lockout threshold

    threshold_patterns = [

        r"\b(?:set|change|lower|reduce|increase|adjust)\b"
        r".{0,60}\b(?:lockout|account lockout)\b"
        r".{0,60}\b(?:threshold|limit)\b"
        r".{0,30}\b\d+\b",

        r"\b(?:lockout|account lockout)\b"
        r".{0,60}\b(?:threshold|limit)\b"
        r".{0,30}\b(?:to|at|of)\s*\d+\b"
    ]

    for pattern in threshold_patterns:

        if re.search(pattern, normalized_recommendations):

            issues.append(
                "Numerical lockout threshold proposed "
                "without verified policy context."
            )

            break

    # CHECK 8: Sensitive actions must require approval

    approval_phrases = [
        "human approval required",
        "human analyst",
        "authorized human",
        "review and approve"
    ]

    if not any(
        phrase in normalized
        for phrase in approval_phrases
    ):

        issues.append(
            "Human approval requirement is missing."
        )

    # FINAL STATUS

    if issues:
        status = "FAIL"

    elif review_items:
        status = "REVIEW"

    else:
        status = "PASS"

    return {
        "status": status,
        "issues": issues,
        "review_items": review_items
    }


# ==================================================
# 8. MAIN CROSS-INCIDENT AGENT
# ==================================================

def run_cross_incident_agent(incident):

    print("\n" + "=" * 65)
    print("SENTINELOPS - CROSS-INCIDENT INTELLIGENCE")
    print("=" * 65)

    validate_incident(incident)

    print("\n[1] Current incident received.")
    print("Incident ID:", incident["incident_id"])

    print("\n[2] Retrieving historical memories from Hindsight...")

    memories = retrieve_related_incidents(incident)

    print(f"Retrieved {len(memories)} memory fragments.")

    print("\n[3] Analysing historical relationships...")

    report = analyse_incident_relationships(
        incident,
        memories
    )

    footer = (
        "HUMAN APPROVAL REQUIRED: All sensitive response actions "
        "must be reviewed and approved by an authorized human analyst "
        "before execution."
    )

    if "human approval required:" not in normalize_text(report):
        report += "\n\n" + footer

    print("\n[4] Running deterministic safety audit...")

    audit = audit_report(
        incident,
        report
    )

    print("\n" + "=" * 65)
    print("CROSS-INCIDENT INTELLIGENCE REPORT")
    print("=" * 65)

    print(report)

    print("\n" + "=" * 65)
    print("DETERMINISTIC AUDIT RESULT")
    print("=" * 65)

    print("FINAL STATUS:", audit["status"])

    if audit["issues"]:

        print("\nSafety issues:")

        for issue in audit["issues"]:
            print("-", issue)

    if audit["review_items"]:

        print("\nReview items:")

        for item in audit["review_items"]:
            print("-", item)

    if not audit["issues"] and not audit["review_items"]:

        print("All configured deterministic checks passed.")

    print("\n" + "=" * 65)
    print("CROSS-INCIDENT ANALYSIS COMPLETED")
    print("=" * 65)

    return {
        "incident": incident,
        "memories": memories,
        "report": report,
        "audit": audit
    }


# ==================================================
# 9. TEST INCIDENT
# ==================================================

if __name__ == "__main__":

    test_incident = {

        "incident_id": "INC-004",

        "type": "Suspicious Login Activity",

        "attack_type": "Possible Brute Force",

        "failed_attempts": 38,

        "time_window_minutes": 2,

        "target": "Privileged Employee Account",

        "unfamiliar_ip": True,

        "successful_login": False,

        "environment": "Synthetic Simulation"
    }

    run_cross_incident_agent(test_incident)
