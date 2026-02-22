from typing import Dict, Any

from engine.agent_base import BaseAgent, Agentinput, Agentoutput
from extensions.llm.gemini import GeminiClient


class AudienceAnalyzerAgent(BaseAgent):
    """
    Analyzes the validated marketing input and extracts
    structured audience insights.

    This is rule based for now (no LLM yet).
    """

    def __init__(self, llm=None):
        super().__init__(
            name="marketing.audience_analyzer",   # runtime unique name
            description="Analyzes target audience and extracts insights",
            input_schema=Agentinput,
            output_schema=Agentoutput,
            allowed_tools=[],
        )

        self.llm = llm or GeminiClient()

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        payload = validated_input.payload  # output from Input validator Agent.

        prompt = f"""
        You are a marketing strategist,

        Analyze the following input and return structured JSON with this format:
        {{
            "pain_points": [],
            "motivations": [],
            "tone": ""
        }}

        Product: {payload.get("product_description")}
        Target audience: {payload.get("target_audience")}
        Goal: {payload.get("goal")}
        """

        llm_response = self.llm.generate_json(prompt)

        insights = {
            "pain_points": llm_response.get("pain_points", []),
            "motivations": llm_response.get("motivations", []),
            "tone": llm_response.get("tone", "professional")
        }

        return Agentoutput(
            output={"audience_insights": insights},
            confidence=0.85,
            metadata={"analyzed_by": self.name},
        )
