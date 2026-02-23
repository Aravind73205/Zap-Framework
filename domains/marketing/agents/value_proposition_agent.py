from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput
from extensions.llm.base import BaseLLM


class ValuePropositionAgent(BaseAgent):
    """
    Generates a compelling value proposition using
    audience insights and product context.
    """

    def __init__(self, llm: BaseLLM):
        super().__init__(
            name="marketing.value_proposition",
            description="Generates core message and key benefits",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

        self.llm = llm

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:

        payload = validated_input.payload

        prompt = f"""
        You are a senior marketing strategist with 15+ years experience

        Based on the audience insights and product context below,
        generate a compelling value proposition.

        Return ONLY valid JSON in this format:
        {{
            "core_message": "",
            "key_benefits": [""],
            "goal": ""
        }}

        Product: {payload.get("product_description")}
        Goal: {payload.get("goal")}

        Audience Pain Points:
        {payload.get("audience_insights", {}).get("pain_points")}

        Audience Motivations:
        {payload.get("audience_insights", {}).get("motivations")}

        Tone:
        {payload.get("audience_insights", {}).get("tone")}
        """

        llm_response = self.llm.generate_json(prompt)

        result = {
            "core_message": llm_response.get("core_message", ""),
            "key_benefits": llm_response.get("key_benefits", []),
            "goal": llm_response.get("goal", ""),
        }

        return Agentoutput(
            output=result,
            confidence=0.9,
            metadata={"generated_by": self.name},
        )
