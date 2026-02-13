from engine.orchestrator import Orchestrator
from domains.marketing.workflow.marketing_workflow import create_marketing_workflow

from domains.marketing.agents.input_validator_agent import InputValidatorAgent
from domains.marketing.agents.audience_analyzer_agent import AudienceAnalyzerAgent
from domains.marketing.agents.value_proposition_agent import ValuePropositionAgent
from domains.marketing.agents.content_outline_generator import ContentOutlineGeneratorAgent


def test_marketing_workflow():
    # Instantiate agents
    input_validator = InputValidatorAgent()
    audience_analyzer = AudienceAnalyzerAgent()
    value_proposition = ValuePropositionAgent()
    content_outline = ContentOutlineGeneratorAgent()


    # Build workflow (only first 2 agents for now)
    steps = create_marketing_workflow(
        input_validator=input_validator,
        audience_analyzer=audience_analyzer,
        value_proposition_agent=value_proposition,       
        content_outline_generator=content_outline,       
    )

    orchestrator = Orchestrator(steps=steps)

    # Sample user input
    initial_input = {
        "payload": {
            "product_description": "AI CRM tool",
            "target_audience": "SaaS founders",
            "goal": "Increase signups"
        },
        "metadata": {"trace": "marketing-test"}
    }

    result = orchestrator.run(initial_input)

    print("\n=== RESULT ===")
    print("STATUS:", result["status"])
    print("FINAL OUTPUT:", result["final_output"].model_dump_json())
    print("\n=== RECORDS ===")
    for rec in result["rec_history"]:
        print(rec.model_dump_json())


if __name__ == "__main__":
    test_marketing_workflow()
