from typing import Dict, Any
from engine.agent_base import BaseAgent, Agentinput, Agentoutput

class DummyAgent(BaseAgent):
    """
    Simple agent used only for testing the execution pipeline.
    Expects payload["n"] and returns n * 2.
    """

    def __init__(self):
        super().__init__(
            name="dummy_agent",
            description="Doubles an integer provided in input.payload['n']",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        n = validated_input.payload.get("n")

        if n is None:
            raise ValueError("Missing 'n' in input.payload")

        if not isinstance(n, (int, float)):
            raise ValueError("'n' must be numeric")

        return Agentoutput(
            output={"value": n * 2},
            confidence=0.95,
            metadata={"source": "dummy"},
        )


def test_base_agent_layer():
    agent = DummyAgent()

    sample_input = {
        "payload": {"n": 5},
        "metadata": {"trace": "test-agent-base"},
    }

    output, record = agent.run(sample_input)

    print("OUTPUT:", output.model_dump_json())
    print("RECORD:", record.model_dump_json())


if __name__ == "__main__":
    test_base_agent_layer()
