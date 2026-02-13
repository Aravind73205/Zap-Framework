from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput


class ContentOutlineGeneratorAgent(BaseAgent):
    """
    Generates a simple marketing content outline
    based on value proposition.
    """

    def __init__(self):
        super().__init__(
            name="marketing.content_outline_generator",
            description="Generates structured marketing content outline",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        payload = validated_input.payload

        core_message = payload.get("core_message")
        key_benefits = payload.get("key_benefits", [])
        goal = payload.get("goal") or "achieve your goals"

        outline = {
            "headline": core_message,
            "introduction": f"Are you struggling to {goal.lower()}?",
            "benefits_section": key_benefits,
            "call_to_action": f"Start today and {goal.lower()} with confidence.",
        }

        return Agentoutput(
            output={"content_outline": outline},
            confidence=0.85,
            metadata={"generated_by": self.name},
        )
