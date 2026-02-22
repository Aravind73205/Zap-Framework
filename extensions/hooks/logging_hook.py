import json
from typing import Any

from engine.hooks import BaseHook
from engine.agent_base import AgentrunRecord


class LoggingHook(BaseHook):
    """
    LoggingHook is an observer.
    It logs workflow and agent lifecycle events.
    It does NOT affect execution.
    """

    #workflow lvl
    def on_workflow_start(self, initial_input: dict) -> None:
        print("\n[LOG] Workflow started")
        print("[LOG] Initial input:")
        print(json.dumps(initial_input, indent=2))

    def on_workflow_end(self, result: dict, rec_history: list) -> None:
        print("\n[LOG] Workflow ended")
        print("[LOG] Status:", result["status"])
        print("[LOG] Total agents run:", len(rec_history))


    # agent lvl
    def before_agent_run(self, agent: Any, agent_input: dict) -> None:
        print(f"\n[LOG] → Running agent: {agent.name}")
        print("[LOG] Agent input:")
        print(json.dumps(agent_input, indent=2))

    def after_agent_run(self, agent: Any, agent_output: Any, record: AgentrunRecord) -> None:
        print(f"[LOG] ← Agent finished: {agent.name}")
        print("[LOG] Status:", record.status)
        print("[LOG] Duration:", f"{record.duration_s:.4f}s")
        print("[LOG] Output:")
        print(json.dumps(agent_output.model_dump(), indent=2))

    def on_agent_error(
        self,
        agent: Any,
        error: Exception,
        record: AgentrunRecord,
    ) -> None:
        print(f"\n[LOG][ERROR] Agent failed: {agent.name}")
        print("[LOG][ERROR] Error:", str(error))
        print("[LOG][ERROR] Record:")
        print(json.dumps(record.model_dump(), indent=2))
