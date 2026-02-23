from extensions.llm.gemini import GeminiClient
from domains.marketing.agents.input_validator_agent import InputValidatorAgent
from domains.marketing.agents.audience_analyzer_agent import AudienceAnalyzerAgent
from domains.marketing.agents.value_proposition_agent import ValuePropositionAgent
from domains.marketing.agents.content_outline_generator import ContentOutlineGeneratorAgent


def build_marketing_agents():

    llm = GeminiClient()

    return {
        "input_validator": InputValidatorAgent(),
        "audience_analyzer": AudienceAnalyzerAgent(llm),
        "value_proposition": ValuePropositionAgent(llm),
        "content_outline": ContentOutlineGeneratorAgent(llm),
    }