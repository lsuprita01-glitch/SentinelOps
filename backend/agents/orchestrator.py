
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from .detective import investigate_incident
    from .memory_agent import recall_incidents
    from .prediction_agent import predict_attack_stages
    from .response_strategist import recommend_response
    from .auditor import audit_investigation
    from .cross_incident_agent import run_cross_incident_agent
except ImportError:
    from detective import investigate_incident
    from memory_agent import recall_incidents
    from prediction_agent import predict_attack_stages
    from response_strategist import recommend_response
    from auditor import audit_investigation
    from cross_incident_agent import run_cross_incident_agent


def run_war_room(incident=None):

    if incident is None:
        incident = {
            "incident_id": "INC-005",
            "type": "Suspicious Login Activity",
            "attack_type": "Possible Brute Force",
            "failed_attempts": 38,
            "time_window_minutes": 2,
            "target": "Privileged Employee Account",
            "unfamiliar_ip": True,
            "successful_login": False,
            "environment": "Synthetic Simulation",
            "source_ip": "192.0.2.45"
        }

    print("\nSENTINELOPS AI WAR ROOM")
    print("=" * 55)
    print("Investigating:", incident.get("incident_id"))

    # AGENT 1: DETECTIVE
    detective_result = investigate_incident(incident)

    # AGENT 2: MEMORY
    memory_query = (
        f"Historical incidents similar to {incident.get('attack_type', 'security incident')}. "
        "Find defensive actions and recorded outcomes."
    )
    historical_memories = recall_incidents(memory_query)

    # AGENT 3: PREDICTION
    predictions = predict_attack_stages(
        incident, historical_memories
    )

    # AGENT 4: RESPONSE STRATEGIST
    recommendations = recommend_response(
        incident,
        detective_result,
        historical_memories,
        predictions
    )

    # AGENT 5: AUDITOR
    audit_result = audit_investigation(
        incident,
        detective_result,
        historical_memories,
        predictions,
        recommendations
    )

    # AGENT 6: CROSS-INCIDENT INTELLIGENCE
    cross_incident_result = run_cross_incident_agent(incident)

    print("\nWAR ROOM COMPLETED")
    print("Incident:", incident.get("incident_id"))
    print("Initial Audit:", audit_result.get("final_status"))
    print(
        "Cross-Incident Audit:",
        cross_incident_result.get("audit", {}).get("status")
    )

    return {
        "incident": incident,
        "detective": detective_result,
        "memories": historical_memories,
        "predictions": predictions,
        "recommendations": recommendations,
        "audit": audit_result,
        "cross_incident": cross_incident_result,
        "agents_executed": 6,
        "simulation_only": True
    }


if __name__ == "__main__":
    result = run_war_room()
    print("\nFinal result:")
    print(result)
