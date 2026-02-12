import json
import os
import time
from typing import List, Optional

from engine.agent_base import AgentrunRecord


class MemoryStore:
    """
    Simple file based storage for keeping workflow run history.
    Saves everything in one json file, not pretty but works for now.
    """

    def __init__(self, file_path: str = "data/memory_store.json"):
        self.file_path = file_path

        # Ensure memory file exists
        if not os.path.exists(self.file_path):
            self._write_json([])

    # Public methods

    def save_workflow_run(self, rec_history: List[AgentrunRecord]) -> None:
        """
        Persist a completed workflow run to memory.
        """
        if not rec_history:
            return

        data = self._read_json()

        entry = {
            "run_id": rec_history[0].run_id,
            "timestamp": time.time(),
            "records": [rec.model_dump() for rec in rec_history],
        }

        data.append(entry)
        self._write_json(data)

    def get_all_runs(self) -> List[dict]:
        """
        Return all stored workflow runs.
        """
        return self._read_json()

    def get_latest(self) -> Optional[dict]:
        """
        Return the most recent workflow run.
        """
        data = self._read_json()
        if not data:
            return None
        return data[-1]

    def clear(self) -> None:
        """
        Wipeout all stored memory, which is useful for testing / debugging
        """
        self._write_json([])

    # internal helpers

    def _read_json(self) -> List[dict]:
        if not os.path.exists(self.file_path):
            return []

        if os.path.getsize(self.file_path) == 0:
            return []
    
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, data: List[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
