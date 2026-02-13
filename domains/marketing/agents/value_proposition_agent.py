from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput


class ValuePropositionAgent(BaseAgent):
    """
    Generates a basic value proposition
    based on validated input + audience insights.
    """

    def __init__(self):
        super().__init__(
            name="marketing.value_proposition",
            description="Generates core message and key benefits",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        payload = validated_input.payload

        product = payload.get("product_description")
        goal = payload.get("goal")
        audience_insights = payload.get("audience_insights", {})

        pain_points = audience_insights.get("pain_points", [])
        motivations = audience_insights.get("motivations", [])

        core_message = f"{product} helps you {goal.lower()} efficiently."
        key_benefits = [
            f"Solve {pain_points[0]}" if pain_points else "Increase efficiency",
            f"Enable {motivations[0]}" if motivations else "Drive growth",
        ]

        return Agentoutput(
            output={
                "core_message": core_message,
                "key_benefits": key_benefits,
                "goal": goal,
            },
            confidence=0.9,
            metadata={"generated_by": self.name},
        )
