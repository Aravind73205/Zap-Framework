from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput
from extensions.llm.base import BaseLLM


class ContentOutlineGeneratorAgent(BaseAgent):
    """
    Generates a structured marketing content outline
    using the value proposition output.
    """

    def __init__(self, llm: BaseLLM):
        super().__init__(
            name="marketing.content_outline_generator",
            description="Generates structured marketing content outline",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

        self.llm = llm

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:

        payload = validated_input.payload

        prompt = f"""
        You are a senior SaaS marketing copywriter with 10+ years of experience.

        Based on the value proposition below, generate a structured
        marketing content outline.

        Return ONLY valid JSON in this format:
        {{
            "headline": "",
            "introduction": "",
            "benefits_section": [
            {{"title": "", "description": ""}},
            ],
            "call_to_action": ""
        }}

        Core Message:
        {payload.get("core_message")}

        Key Benefits:
        {payload.get("key_benefits")}

        Goal:
        {payload.get("goal")}
        """
        llm_response = self.llm.generate_json(prompt)

        result = {
            "headline": llm_response.get("headline", ""),
            "introduction": llm_response.get("introduction", ""),
            "benefits_section": llm_response.get("benefits_section", []),
            "call_to_action": llm_response.get("call_to_action", ""),
        }

        return Agentoutput(
            output={"content_outline": result},
            confidence=0.85,
            metadata={"generated_by": self.name},
        )
