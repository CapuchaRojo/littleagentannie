import re
import json
from collections import defaultdict
from ibm_watsonx import WatsonxFoundationModel  # IBM Granite API

class GoalBasedIncidentAgent:
    def __init__(self, knowledge_base, granite_api_key):
        self.knowledge_base = knowledge_base
        self.incident_logs = []
        self.categorized_incidents = defaultdict(list)
        self.granite_model = WatsonxFoundationModel(api_key=granite_api_key, model_name="granite-nlp")

    def parse_logs(self, log_data):
        """Parses IT logs using IBM Granite NLP for enhanced log understanding."""
        for log in log_data:
            response = self.granite_model.analyze_text(log)
            category = response.get("category", "Unknown")
            suggested_solution = self.knowledge_base.get(category, {}).get("solution", "No predefined solution.")

            self.incident_logs.append((log, category, suggested_solution))
            self.categorized_incidents[category].append(log)

    def diagnose_incidents(self):
        """Generates an incident report with categorized incidents and suggested solutions."""
        report = [{"Log": log, "Category": category, "Suggested Solution": solution}
                  for log, category, solution in self.incident_logs]
        return report

    def recommend_action(self):
        """Suggests proactive steps based on incident severity and frequency."""
        recommendations = {}
        for category, logs in self.categorized_incidents.items():
            if len(logs) > 3:
                recommendations[category] = f"Recurring issue detected. Consider a permanent fix."
        return recommendations

# Sample knowledge base
knowledge_base = {
    "Critical": {"solution": "Restart the server and check logs."},
    "High": {"solution": "Optimize queries or scale database resources."},
    "Medium": {"solution": "Analyze application memory usage and fix leaks."}
}

# Example log data
log_data = [
    "2025-02-22 10:00:01 - Server crashed due to overload.",
    "2025-02-22 10:05:43 - Database timeout on user request.",
    "2025-02-22 10:15:12 - Memory leak detected in process X."
]

# Initialize and run the agent
granite_api_key = "YOUR_IBM_GRANITE_API_KEY"
incident_agent = GoalBasedIncidentAgent(knowledge_base, granite_api_key)
incident_agent.parse_logs(log_data)
incident_report = incident_agent.diagnose_incidents()
action_recommendations = incident_agent.recommend_action()

print("Incident Report:")
print(json.dumps(incident_report, indent=4))
print("\nRecommended Actions:")
print(json.dumps(action_recommendations, indent=4))
