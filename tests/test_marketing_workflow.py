from engine.orchestrator import Orchestrator
from engine.hooks import HookManager

from extensions import llm
from extensions.hooks.logging_hook import LoggingHook
from extensions.hooks.memory_hook import MemoryHook

from domains.marketing.agent_factory import build_marketing_agents
from domains.marketing.workflow.marketing_workflow import create_marketing_workflow


def test_marketing_workflow():

    agents = build_marketing_agents()

    steps = create_marketing_workflow(
        input_validator=agents["input_validator"],
        audience_analyzer=agents["audience_analyzer"],
        value_proposition_agent=agents["value_proposition"],
        content_outline_generator=agents["content_outline"],
    )
    
    # create hook for memory
    hook_manager = HookManager([
        LoggingHook(),
        MemoryHook(),
    ])

    # Create orchestrator
    orchestrator = Orchestrator(
        steps=steps,
        hook_manager=hook_manager,
    )

    # sample user input
    initial_input = {
        "payload": {
            "product_description": "AI CRM tool",
            "target_audience": "SaaS founders",
            "goal": "Increase signups"
        },
        "metadata": {"trace": "marketing-test"}
    }

    result = orchestrator.run(initial_input)

    print("\n RESULT :")
    print("STATUS:", result["status"])
    print("FINAL OUTPUT:", result["final_output"].model_dump_json())
    
    print("\n=== RECORDS ===")
    for rec in result["rec_history"]:
        print(rec.model_dump_json())


if __name__ == "__main__":
    test_marketing_workflow()
