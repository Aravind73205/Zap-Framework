from typing import Dict, Any, List

from engine.agent_base import BaseAgent, Agentinput, Agentoutput


class InputValidatorAgent(BaseAgent):
    """
    Validates and cleans user input for marketing workflow.

    It ensures required keys exist
    Fails fast if something important is missing.
    """

    REQUIRED_KEYS: List[str] = [
        "product_description",
        "target_audience",
        "goal",
    ]

    def __init__(self):
        super().__init__(
            name="marketing.input_validator",   # unique name to avoid conflicts
            description="Validates initial marketing input",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        payload = validated_input.payload     # raw user input comes from cli

        # validation
        for key in self.REQUIRED_KEYS:
            if key not in payload or not payload[key]:
                raise ValueError(f"Missing required input field: '{key}'")

        clean_input = {
            "product_description": str(payload["product_description"]).strip(),
            "target_audience": str(payload["target_audience"]).strip(),
            "goal": str(payload["goal"]).strip(),
        }

        return Agentoutput(
            output={"validated_input": clean_input},
            confidence=1.0,
            metadata={"validated_by": self.name},
        )
