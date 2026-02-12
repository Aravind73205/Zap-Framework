from typing import Any, List

from engine.guardrails import GuardrailViolation


class BaseHook:
    """
    Base class for hooks

    They are just observers. They do not:
    - stop or change the flow
    - modify the actual input/output data
    - decide workflow outcome

    We can pick and choose which methods to override.
    Missing methods are automatically ignored, so no worries.
    """

    # workflow lvl stuff
    def on_workflow_start(self, initial_input: dict) -> None:
        pass

    def on_workflow_end(self, result: dict, rec_history: list) -> None:
        pass


    # per agent hooks
    def before_agent_run(self, agent: Any, agent_input: dict) -> None:
        pass

    def after_agent_run(self, agent: Any, agent_output: Any, record: Any) -> None:
        pass

    def on_agent_error(self, agent: Any, error: Exception, record: Any) -> None:
        pass


class HookManager:
    """
    Just a simple thing that calls all the hooks one by one

    orchestrator will use this to fire hook events
    without knowing what hooks actually do.
    """

    def __init__(self, hooks: List[BaseHook] | None = None):
        self.hooks = hooks or []

    #internal method
    def _call(self, method_name: str, *args) -> None:
        for hook in self.hooks:
            callback = getattr(hook, method_name, None)
            if callable(callback):               
                try:
                    callback(*args)

                except GuardrailViolation:
                    raise         # let guardrails kill the run

                except Exception as e:
                    # very important: hooks must not crash everything
                    print(f"[HookManager] Hook error in {method_name}: {e}")


    # Public methods — these are the ones the orchestrator calls
    def workflow_start(self, initial_input: dict) -> None:
        self._call("on_workflow_start", initial_input)

    def workflow_end(self, result: dict, rec_history: list) -> None:
        self._call("on_workflow_end", result, rec_history)

    def before_agent(self, agent: Any, agent_input: dict) -> None:
        self._call("before_agent_run", agent, agent_input)

    def after_agent(self, agent: Any, agent_output: Any, record: Any) -> None:
        self._call("after_agent_run", agent, agent_output, record)

    def agent_error(self, agent: Any, error: Exception, record: Any) -> None:
        self._call("on_agent_error", agent, error, record)
