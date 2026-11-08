
import os
import re
import unicodedata

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "sentinelops-security-memory"
GROQ_MODEL = "openai/gpt-oss-120b"


# --------------------------------------------------
# CONNECTIONS
# --------------------------------------------------

def connect_hindsight():
    api_key = os.getenv("HINDSIGHT_API_KEY")
    base_url = os.getenv("HINDSIGHT_BASE_URL")

    if not api_key or not base_url:
        raise ValueError("Hindsight credentials missing from .env")

    return Hindsight(base_url=base_url, api_key=api_key)


def connect_groq():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing from .env")

    return Groq(api_key=api_key)


# --------------------------------------------------
# VALIDATE INCIDENT
# --------------------------------------------------

def validate_incident(incident):

    required = [
        "incident_id",
        "type",
        "failed_attempts",
        "time_window_minutes",
        "target",
        "unfamiliar_ip",
        "successful_login",
        "environment"
    ]

    missing = [key for key in required if key not in incident]

    if missing:
        raise ValueError(f"Missing fields: {missing}")

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


# --------------------------------------------------
# RETRIEVE HINDSIGHT MEMORIES
# --------------------------------------------------

def retrieve_related_incidents(incident):

    client = connect_hindsight()

    query = (
        f"Previous cybersecurity incidents involving "
        f"{incident['type']}, failed logins, brute force, "
        f"employee accounts, defensive actions and outcomes."
    )

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        memories = []

        if result and result.results:
            for item in result.results[:10]:
                if getattr(item, "text", None):
                    memories.append(item.text)

        return memories

    finally:
        close_method = getattr(client, "close", None)

        if callable(close_method):
            close_method()


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize_text(text):

    text = unicodedata.normalize("NFKC", str(text))

    for character in ["\u2010", "\u2011", "\u2012",
                      "\u2013", "\u2014", "\u2212"]:
        text = text.replace(character, "-")

    return text.lower()


def clean_heading(line):

    line = normalize_text(line).strip()

    # Remove Markdown formatting around headings.
    line = re.sub(r"^[\s#>*`]+", "", line)
    line = re.sub(r"[\s*`]+$", "", line)

    return line.strip()


# --------------------------------------------------
# EXTRACT NUMBERED REPORT SECTIONS
# --------------------------------------------------

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


# --------------------------------------------------
# AI CROSS-INCIDENT ANALYSIS
# --------------------------------------------------

def analyse_incident_relationships(incident, memories):

    groq = connect_groq()

    source_ip = incident.get("source_ip")

    current_incident = f"""
CURRENT INCIDENT:

Incident ID: {incident['incident_id']}
Type: {incident['type']}
Failed attempts: {incident['failed_attempts']}
Time window: {incident['time_window_minutes']} minutes
Target: {incident['target']}
Unfamiliar IP indicator: {incident['unfamiliar_ip']}
Successful login recorded: {incident['successful_login']}
Environment: {incident['environment']}
Exact source IP supplied: {bool(source_ip)}
"""

    memory_context = (
        "\n".join(f"- {memory}" for memory in memories)
        if memories
        else "No historical memories retrieved."
    )

    prompt = f"""
You are the Cross-Incident Intelligence Agent of SentinelOps.

{current_incident}

HISTORICAL HINDSIGHT MEMORIES:

{memory_context}

STRICT RULES:

1. Separate current facts from historical memories.
2. Never invent IP addresses, usernames, hostnames or assets.
3. Similar attempt counts are behavioral similarities, not shared indicators.
4. An unfamiliar IP does not prove a historical IP match.
5. Do not recommend IP blocking without an exact source IP.
6. Do not invent numerical lockout thresholds.
7. Do not assume historical MFA settings apply to the current account.
8. False successful_login means no success is recorded in supplied data.
9. Predictions must be labelled as hypotheses.
10. Sensitive changes require human approval.
11. Do not invent confidence percentages.
12. If there are no exact matching technical indicators, state:
    No verified shared indicators found.
13. Historical simulation results do not guarantee future results.
14. Do not claim that historical controls are proven effective in
    real-world environments based only on synthetic simulations.

Use these exact headings:

1. CURRENT INCIDENT SUMMARY

2. HISTORICAL INCIDENTS RETRIEVED

3. EVIDENCE-BACKED SIMILARITIES

4. SHARED TECHNICAL INDICATORS

5. HISTORICAL RESPONSE AND OUTCOME

6. INTELLIGENCE GAPS

7. RELATIONSHIP CONFIDENCE

8. RECOMMENDATIONS

9. CONCLUSION

The report must finish with:

HUMAN APPROVAL REQUIRED: All sensitive response actions must be
reviewed and approved by an authorized human analyst before execution.
"""

    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cautious cybersecurity analyst. "
                    "Never invent evidence or confuse historical "
                    "information with current incident facts."
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


# --------------------------------------------------
# DETERMINISTIC AUDIT
# --------------------------------------------------

def audit_report(incident, report):

    issues = []
    review_items = []

    normalized = normalize_text(report)

    # Extract sections using the corrected Markdown parser.
    sections = {
        3: extract_section(report, 3, 4),
        4: extract_section(report, 4, 5),
        8: extract_section(report, 8, 9)
    }

    similarities = sections[3]
    shared = sections[4]
    recommendations = sections[8]

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

    # CHECK 2: Section 3 must exist.

    if not similarities.strip():
        issues.append("Evidence-backed similarities section is empty.")

    # CHECK 3: Section 4 must exist.

    if not shared.strip():
        issues.append("Shared technical indicators section is empty.")

    # CHECK 4: Do not mistake behavioral similarities for shared indicators.

    behavioral_terms = [
        "failed attempts",
        "failed login attempts",
        "time window",
        "login attempts",
        "minutes"
    ]

    if (
        "no verified shared indicators found" not in normalized_shared
        and any(term in normalized_shared for term in behavioral_terms)
    ):
        review_items.append(
            "Check whether behavioral similarities have been "
            "incorrectly described as shared technical indicators."
        )

    # CHECK 5: Unsupported successful-login claims.

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

    # CHECK 6: No IP blocking without exact IP.

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
                    "IP or network blocking recommended without "
                    "an exact verified source IP."
                )
                break

    # CHECK 7: Numerical lockout threshold.

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
                "Numerical lockout threshold proposed without "
                "verified policy context."
            )
            break

    # CHECK 8: Human approval.

    approval_phrases = [
        "human approval required",
        "human analyst",
        "authorized human",
        "review and approve"
    ]

    if not any(phrase in normalized for phrase in approval_phrases):
        issues.append("Human approval requirement is missing.")

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


# --------------------------------------------------
# MAIN AGENT
# --------------------------------------------------

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

    if "HUMAN APPROVAL REQUIRED:" not in report.upper():
        report += "\n\n" + footer

    print("\n[4] Running deterministic safety audit...")

    audit = audit_report(incident, report)

    print("\n" + "=" * 65)
    print("CROSS-INCIDENT INTELLIGENCE REPORT")
    print("=" * 65)

    print(report)

    print("\n" + "=" * 65)
    print("DETERMINISTIC AUDIT RESULT")
    print("=" * 65)

    print("FINAL STATUS:", audit["status"])

    if audit["issues"]:
        print("\nIssues:")
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


# --------------------------------------------------
# TEST INCIDENT
# --------------------------------------------------

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
