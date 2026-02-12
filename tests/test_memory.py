from engine.memory import MemoryStore
from engine.agent_base import AgentrunRecord
import time
import uuid

def make_dummy_record(agent_name: str, result: int):
    start_ts = time.time()
    end_ts = start_ts + 0.02

    return AgentrunRecord(
        run_id=str(uuid.uuid4()),
        agent_name=agent_name,
        start_ts=start_ts,
        end_ts=end_ts,                 # Required (can be None, but must exist)
        duration_s=end_ts - start_ts,  # Required (can be None, but must exist)
        status="success",
        input={"n": 10},
        output={"result": result},     # Required (can be None)
        error=None,                    # Required
        tokens_used=None,
        extra={},                      # optional, but explicit is clean
    )

if __name__ == "__main__":
    memory = MemoryStore()

    # fake workflow history (like orchestrator would produce)
    rec_history = [
        make_dummy_record("dummy_agent", 20),
        make_dummy_record("dummy_agent_2", 40),
    ]

    # store it
    memory.save_workflow_run(rec_history)

    # read it back
    all_runs = memory.get_all_runs()
    last_run = memory.get_latest()

    print("TOTAL RUNS:", len(all_runs))
    print("LAST RUN:")
    print(last_run)
