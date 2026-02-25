from dotenv import load_dotenv
load_dotenv()

from engine.orchestrator import Orchestrator
from engine.hooks import HookManager

from extensions.hooks.logging_hook import LoggingHook
from extensions.hooks.memory_hook import MemoryHook

from domains.marketing.agent_factory import build_marketing_agents
from domains.marketing.workflow.marketing_workflow import create_marketing_workflow


def main():
    agents = build_marketing_agents()

    steps = create_marketing_workflow(
        input_validator=agents["input_validator"],
        audience_analyzer=agents["audience_analyzer"],
        value_proposition_agent=agents["value_proposition"],
        content_outline_generator=agents["content_outline"],
    )

    orchestrator = Orchestrator(
        steps=steps,
        hook_manager=HookManager([
            LoggingHook(),
            MemoryHook(),
        ])
    )

    user_input = {
        "payload": {
            "product_description": "AI CRM tool",
            "target_audience": "SaaS founders",
            "goal": "Increase signups"
        },
        "metadata": {"trace": "cli-run"}
    }

    result = orchestrator.run(user_input)

    print("\n=== FINAL RESULT ===")
    print(result["final_output"].model_dump_json(indent=2))


if __name__ == "__main__":
    main()