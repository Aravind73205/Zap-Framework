from typing import Any, List, Optional

from engine.hooks import BaseHook
from engine.guardrails import GuardrailViolation

class GuardrailHook(BaseHook):
    """
    Enforces basic safety rules and policies.

    It can:
    - stop a workflow early
    - reject invalid inputs

    It should raise GuardrailViolation on failure.
    """

    def __init__(
        self,
        max_steps: Optional[int] = None,                              # eg : 15 to prevent infinite loops
        required_input_keys: Optional[List[str]] = None,
        blocked_agents: Optional[List[str]] = None,
    ):
        self.max_steps = max_steps
        self.required_input_keys = required_input_keys or []
        self.blocked_agents = blocked_agents or []

        self._step_count = 0

    # workflow lvl 

    def on_workflow_start(self, initial_input: dict) -> None:
        self._step_count = 0

        if self.required_input_keys:
            payload = initial_input.get("payload", {})
            for key in self.required_input_keys:
                if key not in payload:
                    raise GuardrailViolation(
                        f"Missing required input key: '{key}'"
                    )

    # agent lvl

    def before_agent_run(self, agent: Any, agent_input: dict) -> None:
        self._step_count += 1

        if self.max_steps is not None and self._step_count > self.max_steps:
            raise GuardrailViolation(
                f"Workflow exceeded max steps ({self.max_steps})"
            )

        if agent.name in self.blocked_agents:
            raise GuardrailViolation(
                f"Agent '{agent.name}' is blocked by guardrails"
            )
