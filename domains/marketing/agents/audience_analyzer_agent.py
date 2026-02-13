from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput


class AudienceAnalyzerAgent(BaseAgent):
    """
    Analyzes the validated marketing input and extracts
    structured audience insights.

    This is rule based for now (no LLM yet).
    """

    def __init__(self):
        super().__init__(
            name="marketing.audience_analyzer",   # runtime unique name
            description="Analyzes target audience and extracts insights",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        payload = validated_input.payload  # output from Input validator Agent.

        target_audience = payload.get("target_audience", "").lower()

        # Simple rule based analysis for now 
        insights = {
            "pain_points": [],
            "motivations": [],
            "tone": "professional"
        }

        if "founder" in target_audience:
            insights["pain_points"].append("limited time")
            insights["motivations"].append("growth and scalability")
            insights["tone"] = "confident"

        if "student" in target_audience:
            insights["pain_points"].append("budget constraints")
            insights["motivations"].append("career growth")
            insights["tone"] = "encouraging"

        if not insights["pain_points"]:
            insights["pain_points"].append("general inefficiency")
            insights["motivations"].append("improved outcomes")

        return Agentoutput(
            output={"audience_insights": insights},
            confidence=0.85,
            metadata={"analyzed_by": self.name},
        )
