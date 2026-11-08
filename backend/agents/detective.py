
def investigate_incident(incident):

    print("\n========== DETECTIVE AGENT ==========")
    print("Investigating incoming security event...")

    failed_attempts = incident.get("failed_attempts", 0)
    time_window = incident.get("time_window_minutes")
    target = incident.get("target", "Unknown")
    unfamiliar_ip = incident.get("unfamiliar_ip", False)
    successful_login = incident.get("successful_login", False)

    evidence = []

    # Record supplied incident evidence
    evidence.append(
        f"{failed_attempts} failed login attempts recorded."
    )

    if time_window is not None:
        evidence.append(
            f"Attempts occurred within {time_window} minutes."
        )

    evidence.append(f"Target account: {target}.")

    if unfamiliar_ip:
        evidence.append(
            "An unfamiliar simulated IP indicator was reported."
        )

    if successful_login:
        evidence.append(
            "A successful login is recorded in the supplied event data."
        )
    else:
        evidence.append(
            "No successful login is recorded in the supplied event data."
        )

    # Classify incident
    if successful_login:
        classification = "Potential account compromise"
        severity = "Critical"

    elif failed_attempts >= 25 and "privileged" in target.lower():
        classification = "Suspicious privileged-account login activity"
        severity = "High"

    elif failed_attempts >= 10:
        classification = "Possible brute-force activity"
        severity = "Medium"

    else:
        classification = "Unusual login activity"
        severity = "Low"

    result = {
        "incident_id": incident.get("incident_id", "Unknown"),
        "classification": classification,
        "severity": severity,
        "confirmed_evidence": evidence,
        "successful_login_recorded": successful_login,
        "unfamiliar_ip_reported": unfamiliar_ip,
        "missing_information": [
            "Actual source IP address",
            "Authentication log source",
            "Whether MFA is enabled"
        ],
        "requires_further_investigation": True
    }

    print("\nCLASSIFICATION:", classification)
    print("SEVERITY:", severity)

    print("\nAVAILABLE EVIDENCE:")

    for item in evidence:
        print("-", item)

    print("\nDetective investigation completed.")

    return result
