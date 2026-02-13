from typing import Any, Dict, List, Optional, Callable

from engine.agent_base import BaseAgent, Agentoutput, AgentrunRecord
from engine.hooks import HookManager


class WorkflowStep:
    """
    This exists mainly to decouple agent execution from
    how inputs are transformed between agents. 

    - agent: the agent to run
    - input_transformer: optional fn to convert previous output
                    into this agents input 
    """

    def __init__(
        self,
        agent: BaseAgent,
        input_transformer: Optional[Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        self.agent = agent
        self.input_transformer = input_transformer


class Orchestrator:
    """
    Coordinates execution of multiple agents in sequence

    kept intentionally simple for now — retries, branching,
    and parallelism can be layered on later.
    """

    def __init__(
        self, 
        steps: List[WorkflowStep], 
        hook_manager: Optional[HookManager] = None,
    ):
        if not steps:
            raise ValueError("workflow needs atleast one step...")

        self.steps = steps
        self.hooks = hook_manager

    def run(self, initial_input: Dict[str, Any], context: Optional[Dict[str, Any]] = None,) -> Dict[str, Any]:
        """
        Execute the workflow

        returns:
        {
            status: success | error,
            final output: Agentoutput | none,
            rec history: List[Agentrunrecord]
        }
        """
        # shared mutable state across agents
        context = context or {}
        rec_history: List[AgentrunRecord] = []

        current_input = initial_input

        #workflow start 
        if self.hooks:
            self.hooks.workflow_start(initial_input)

        for step in self.steps:
            agent = step.agent
            print(f"\n[Orch] running agent: {agent.name}")

            if step.input_transformer:
                next_payload = step.input_transformer(
                    current_input["payload"],
                    context,
                )
                step_input = {
                    "payload": next_payload,
                    "metadata": current_input.get("metadata", {}),
                }
            else:
                step_input = current_input

             #before agent
            if self.hooks:
                self.hooks.before_agent(agent, step_input)

            output, record = agent.run(
                raw_input=step_input,
                context=context,
            )

            rec_history.append(record)

            # if agent failed → stop workflow
            # fail fast for now, can add retries later
            if record.status != "success":
                if self.hooks:
                    self.hooks.agent_error(agent, record.error, record) #agent failur hook

                result = {
                    "status": "error",
                    "final_output": output,
                    "rec_history": rec_history,
                }
            
                if self.hooks:
                    self.hooks.workflow_end(result, rec_history)

                return result
            
            #after agent
            if self.hooks:
                self.hooks.after_agent(agent, output, record)

            # on success update context
            context[agent.name] = output.output

            # preparing input for next step          
            current_input = {
                "payload": output.output,
                "metadata": {
                    "previous_agent": agent.name
                }
            }

        result = {
            "status": "success",
            "final_output": output,
            "rec_history": rec_history,
        }
        
        #workflow end
        if self.hooks:
            self.hooks.workflow_end(result, rec_history)

        return result
