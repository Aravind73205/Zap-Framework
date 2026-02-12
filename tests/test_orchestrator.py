# self test with Dummyagent
# This test focuses on orchestration wiring, not on agent logic correctness.

from typing import Dict, Any

from engine.orchestrator import Orchestrator, WorkflowStep
from engine.hooks import HookManager
from extensions.logging_hook import LoggingHook
from extensions.memory_hook import MemoryHook
from extensions.guardrail_hook import GuardrailHook
from tests.test_agent_base import DummyAgent


def test_orch_layer():
    agent1 = DummyAgent()
    agent2 = DummyAgent()

    # Adapter: convert {"value": x} -> {"n": x}
    def prepare_next_input(prev_output: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"n": prev_output["value"]}

    steps = [
        WorkflowStep(agent=agent1),
        WorkflowStep(agent=agent2, input_transformer=prepare_next_input),
    ]

    hooks = HookManager(
        hooks=[
            LoggingHook(),
            MemoryHook(),
            GuardrailHook(
                max_steps=2,
                required_input_keys=["n"],
                blocked_agents=[],
            ),
        ]
    )

    orchestrator = Orchestrator(steps=steps, hook_manager=hooks)

    initial_input = {
        "payload": {"n": 5},
        "metadata": {"trace": "workflow adapter test"},
    }

    result = orchestrator.run(initial_input)

    print("\n=== WORKFLOW RESULT ===")
    print("STATUS:", result["status"])

    if result["final_output"] is not None:
        print("FINAL OUTPUT:", result["final_output"].model_dump_json())
    else:
        print("FINAL OUTPUT: None (workflow stopped early)")

    print("\n=== RUN RECORDS ===")
    for rec in result["rec_history"]:
        print(rec.model_dump_json())

if __name__ == "__main__":
    test_orch_layer()