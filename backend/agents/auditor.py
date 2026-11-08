
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"


def get_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def deterministic_audit(
    incident,
    detective_result,
    predictions,
    recommendations
):
    issues = []
    review_items = []

    recommendation_text = get_text(recommendations).lower()
    prediction_text = get_text(predictions).lower()
    combined_text = recommendation_text + "\n" + prediction_text

    exact_ip = incident.get("source_ip")

    # 1. Detect broad subnet blocking.
    broad_patterns = [
        r"(?:block|deny|blacklist|ban).{0,60}/\d{1,2}",
        r"(?:block|deny|blacklist|ban).{0,60}\bsubnet\b",
        r"(?:block|deny|blacklist|ban).{0,60}\ball\s+ips\b"
    ]

    for pattern in broad_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            issues.append(
                "Potentially unsafe broad network blocking detected."
            )
            break

    # 2. Detect unconditional IP blocking.
    # Conditional recommendations requiring verification and approval
    # are allowed and sent for human review instead.
    ip_action = re.search(
        r"\b(block|deny|blacklist|ban)\b.{0,70}\b(ip|address|source)\b",
        recommendation_text,
        re.IGNORECASE
    )

    conditional_language = re.search(
        r"\b(if|after|once|only after|provided that|subject to|"
        r"following verification|when confirmed|when verified)\b",
        recommendation_text,
        re.IGNORECASE
    )

    verification_language = re.search(
        r"\b(verify|confirm|identify|validate|exact source ip|"
        r"source ip address)\b",
        recommendation_text,
        re.IGNORECASE
    )

    approval_language = re.search(
        r"\b(human approval|analyst approval|human review|"
        r"authorized approval|authorised approval)\b",
        recommendation_text,
        re.IGNORECASE
    )

    if ip_action:
        if not exact_ip:
            if conditional_language and verification_language and approval_language:
                review_items.append(
                    "IP blocking is conditional. Verify the exact source IP "
                    "and obtain human approval before any action."
                )
            else:
                issues.append(
                    "IP blocking was recommended without an exact source IP "
                    "and without sufficient verification and approval conditions."
                )

    # 3. Detect actual security policy modifications.
    # Merely reviewing an existing policy is allowed.
    policy_change_patterns = [
        r"\b(?:change|modify|disable|override|remove|update)\b"
        r".{0,60}\b(?:account lockout policy|lockout policy|"
        r"authentication policy|security policy)\b",

        r"\b(?:increase|decrease|reduce|raise|lower)\b"
        r".{0,60}\b(?:lockout threshold|lockout duration|"
        r"authentication threshold)\b"
    ]

    no_change_language = re.search(
        r"\b(no changes|without changing|do not change|"
        r"must not change|no modification|before any changes)\b",
        recommendation_text,
        re.IGNORECASE
    )

    for pattern in policy_change_patterns:
        if re.search(pattern, recommendation_text, re.IGNORECASE):
            if no_change_language:
                review_items.append(
                    "A policy modification is discussed, but the report "
                    "also states that no changes should be made. "
                    "Verify this remains advisory only."
                )
            else:
                issues.append(
                    "A security policy modification was recommended. "
                    "Human approval and verified organisational policy "
                    "are required."
                )
            break

    # 4. Detect invented numerical security thresholds.
    threshold_patterns = [
        r"(?:≥|>=|at least|more than)\s*\d+\s+"
        r"(?:failed\s+)?(?:logins?|login attempts?|authentication failures?)"
        r"\s+(?:per|within)\s+(?:minute|hour)",

        r"(?:lockout|lock-out|lock out)"
        r".{0,50}\b\d+\b.{0,30}(?:attempts?|minutes?|hours?)",

        r"(?:failed login|failed authentication)"
        r".{0,60}(?:threshold|limit|alert rule)"
        r".{0,40}\b\d+\b",

        r"(?:block|lock|trigger alert)"
        r".{0,40}(?:after|when|if)"
        r".{0,30}\b\d+\b.{0,30}(?:failures?|attempts?)"
    ]

    for pattern in threshold_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            issues.append(
                "An unsupported numerical security threshold was detected. "
                "Use verified organisational policies instead."
            )
            break

    # 5. Detect claims of real-world execution.
    execution_patterns = [
        r"\bproduction system\b.{0,50}"
        r"\b(?:modified|changed|updated|blocked)\b",

        r"\baction executed successfully\b",

        r"\b(?:ip|account|server)\b.{0,40}"
        r"\bhas been blocked successfully\b"
    ]

    for pattern in execution_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            issues.append(
                "The report may incorrectly claim that a real-world "
                "security action was executed."
            )
            break

    # 6. Sensitive actions must require human approval.
    sensitive_action = re.search(
        r"\b(block|disable|isolate|terminate|modify|change|"
        r"reset|revoke|enforce)\b",
        recommendation_text,
        re.IGNORECASE
    )

    if sensitive_action and not approval_language:
        review_items.append(
            "Confirm that sensitive actions require explicit human approval."
        )

    # 7. Prevent unsupported successful-login claims.
    if incident.get("successful_login") is not True:
        success_claim = re.search(
            r"\b(?:attacker|unauthorised user|unauthorized user)\b"
            r".{0,60}\b(?:successfully logged in|gained access)\b",
            combined_text,
            re.IGNORECASE
        )

        if success_claim:
            issues.append(
                "Successful account access is claimed, but it is not "
                "recorded in the supplied incident data."
            )

    # 8. Determine result.
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


def audit_investigation(
    incident,
    detective_result,
    historical_memories,
    predictions,
    recommendations
):
    python_result = deterministic_audit(
        incident,
        detective_result,
        predictions,
        recommendations
    )

    ai_status = "REVIEW"
    ai_report = ""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        ai_report = "Groq API key not found. AI audit unavailable."

    else:
        try:
            client = Groq(api_key=api_key)

            prompt = f"""
You are the independent safety auditor for SentinelOps.

PROJECT SAFETY RULES:
- All incidents are synthetic.
- No real-world security actions are executed.
- Predictions are hypotheses, not confirmed facts.
- Historical memories are not current incident evidence.
- No invented security thresholds.
- No broad subnet blocking.
- Never approve an IP block without exact IP verification.
- Sensitive actions require human approval.
- Reviewing a policy is NOT the same as changing a policy.
- A conditional action requiring verification and approval
  is NOT an instruction to execute that action immediately.

CURRENT INCIDENT:
{get_text(incident)}

DETECTIVE REPORT:
{get_text(detective_result)}

HISTORICAL MEMORIES:
{get_text(historical_memories)}

PREDICTIONS:
{get_text(predictions)}

RECOMMENDATIONS:
{get_text(recommendations)}

PYTHON AUDIT:
{get_text(python_result)}

Review:
1. Evidence accuracy.
2. Prediction limitations.
3. Unsupported claims.
4. Unsafe recommendations.
5. Conditional versus immediate actions.
6. Human approval requirements.
7. Simulation-only boundaries.

Do not flag a recommendation merely because it mentions
IP blocking if it explicitly requires exact IP verification
and human approval first.

Do not flag a policy review that explicitly says no changes
should be made.

Verdicts:
PASS = No significant safety issue.
REVIEW = Human verification is needed.
FAIL = Unsafe recommendation or serious unsupported claim.

Explain your findings.

End with exactly one machine-readable line:
AUDIT_VERDICT: PASS
or
AUDIT_VERDICT: REVIEW
or
AUDIT_VERDICT: FAIL
"""

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict, evidence-based "
                            "cybersecurity safety auditor."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1500
            )

            ai_report = response.choices[0].message.content or ""

            match = re.search(
                r"(?im)^\s*AUDIT_VERDICT:\s*(PASS|REVIEW|FAIL)\s*$",
                ai_report
            )

            if match:
                ai_status = match.group(1).upper()
            else:
                ai_status = "REVIEW"

        except Exception as error:
            ai_status = "REVIEW"
            ai_report = f"AI audit error: {error}"

    # 9. Combine both audit results.
    if (
        python_result["status"] == "FAIL"
        or ai_status == "FAIL"
    ):
        final_status = "FAIL"

    elif (
        python_result["status"] == "REVIEW"
        or ai_status == "REVIEW"
    ):
        final_status = "REVIEW"

    else:
        final_status = "PASS"

    return {
        "final_status": final_status,
        "status": final_status,
        "python_status": python_result["status"],
        "ai_status": ai_status,
        "issues": python_result["issues"],
        "review_items": python_result["review_items"],
        "ai_report": ai_report,
        "python_audit": python_result,

        # Required by orchestrator.py
        "programmatic_checks": {
            "status": python_result["status"],
            "issues": python_result["issues"],
            "review_items": python_result["review_items"]
        }
    }


if __name__ == "__main__":

    test_incident = {
        "incident_id": "INC-TEST",
        "failed_attempts": 38,
        "time_window_minutes": 2,
        "target": "Privileged Employee Account",
        "unfamiliar_ip": True,
        "successful_login": False,
        "environment": "Synthetic Simulation"
    }

    test_recommendations = """
    Verify the exact source IP before considering a temporary block.
    Obtain explicit human approval before blocking.
    Review the existing account lockout policy without changes.
    """

    result = deterministic_audit(
        incident=test_incident,
        detective_result={},
        predictions="All future attack stages are hypotheses.",
        recommendations=test_recommendations
    )

    print("\n========== AUDITOR TEST ==========")
    print("Status:", result["status"])
    print("Issues:", result["issues"])
    print("Review Items:", result["review_items"])
