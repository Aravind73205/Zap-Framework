from engine.hooks import BaseHook
from engine.memory import MemoryStore


class MemoryHook(BaseHook):
    """
    Hook that saves completed workflow runs using MemoryStore.

    Only cares about on_workflow_end.
    Saves both successful and failed runs.
    """

    def __init__(self, memory_store: MemoryStore | None = None):
        # allow dependency injection for testing
        self.memory_store = memory_store or MemoryStore()

    def on_workflow_end(self, result: dict, rec_history: list) -> None:
        # store only successful or failed workflows alike
        if not rec_history:
            return

        self.memory_store.save_workflow_run(rec_history)
        # TODO: later we can add success/failure filter or separate failed runs folder