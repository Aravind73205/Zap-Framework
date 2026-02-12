from __future__ import annotations
import time
import uuid
import traceback
from typing import Any, Dict, Iterable, List, Optional, Protocol, Tuple
from pydantic import BaseModel, Field, ValidationError

# Tool interface

class Tool(Protocol):
    name: str          

    def run(self, **kwargs) -> Any:
        ...

# Standard schemas

class Agentinput(BaseModel):
    """
    Agents should rely on `payload` for task related data,
    and `metadata` used for tracing, routing, and etcc
    """
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Agentoutput(BaseModel):
    """
    Confidence is optional but useful later for ranking and etc
    """
    output: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# execution log record (added for debug by reading run records)

class AgentrunRecord(BaseModel):
    run_id: str
    agent_name: str
    start_ts: float
    end_ts: Optional[float]           
    duration_s: Optional[float]
    status: str                       # success | error
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]]  # doesnt exist on error
    error: Optional[str]              # doesnt exist on success

    # TODO:populate this once llm based tools are integrated (eg: openai token accounting) 
    tokens_used: Optional[int] = None

    extra: Dict[str, Any] = Field(default_factory=dict)


# Hooks

HookFn = Any  


# BaseAgent

class BaseAgent:
    """
    base class for all agents in the system

    Design goals:
    - Strict input/output contracts (pydantic)
    - clear execution lifecycle
    - hooks for observability (not control)
    - Safe failure behavior for orchestration
    """

    # attributes that class expected to have(kinda class annotations)
    name: str   
    description: str
    input_schema: BaseModel  
    output_schema: BaseModel  
    allowed_tools: Iterable[str]

    # criteria required to create a agent,(To create an agent, you must provide these)
    def __init__(
        self,
        name: str,
        description: str = "",
        input_schema: type = Agentinput,
        output_schema: type = Agentoutput,
        allowed_tools: Optional[Iterable[str]] = None,
        hooks: Optional[Dict[str, List[HookFn]]] = None,
    ):
    # store values in the instance
        self.name = name
        self.description = description or "" 
        self.input_schema = input_schema
        self.output_schema = output_schema

        self.allowed_tools = set(allowed_tools or [])
        self.tools: Dict[str, Tool] = {}

        #hooks are grouped by lifecycle phase
        self.hooks = hooks or {"before": [], "after": [], "on_error": []}

    # Tool management
    
    def register_tool(self, tool_name: str, tool: Tool):
        """Register the tool instance"""
        self.tools[tool_name] = tool

    def get_tool(self, tool_name: str) -> Tool:
        """Fetch a tool if it is both allowed and registered"""
        if tool_name not in self.allowed_tools:
            raise KeyError(f"Tool '{tool_name}' is not allowed for agent '{self.name}'.")
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' not registered in agent '{self.name}'.")
        return self.tools[tool_name]

    
    #hooks
    
    def add_hook(self, when: str, fn: HookFn):
        if when not in self.hooks:
            raise ValueError(f"Unknown hook phase '{when}'")
        self.hooks[when].append(fn)

    def _run_hooks(self, when: str, record: AgentrunRecord):
        for fn in self.hooks.get(when, []):
            try:
                fn(self, record)
            except Exception:
                print(f"[HOOK ERROR] agent={self.name} hook={when} error={traceback.format_exc()}")

    
    # Implementing (lifecycle contract) 
    # A contract means, (if you want to plug into this system, you must follow these rules)

    def prepare(self, validated_input: Agentinput, context: Dict[str, Any]) -> None: 
        """
        Optional hook before execute

        Typical uses:
        - warm up models
        - validate tool availability
        - enrich context
        """
        return None

    def execute(self, validated_input: Agentinput, context: Dict[str, Any]) -> Agentoutput:
        """
        Core agent logic
        must be implemented by subclasses
        """
        raise NotImplementedError("Agents must implement execute(...)")

    def finalize(self, validated_input: Agentinput, result: Agentoutput, context: Dict[str, Any]) -> None:
        """
        Optional override
        called after a successful execute
        """
        return None

   
    # run wrapper called by orchestrator
    
    def run(
        self, 
        raw_input: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    )-> Tuple[Agentoutput, AgentrunRecord]:
        """
        This wrapper is intentionally defensive, it ensures that:

          - Validate input against input_schema
          - call hooks 'before'
          - prepare -> execute -> finalize
          - validate output against output_schema
          - return (agentoutput, agentrunrecord)
        """
        run_id = str(uuid.uuid4())
        start_ts = time.time()
        context = context or {}
        # TODO: context is mutable for simplicity, this may be revisited if stronger agent isolation  or immutability guarantees are required.

        record = AgentrunRecord(
            run_id=run_id,
            agent_name=self.name,
            start_ts=start_ts,
            end_ts=None,
            duration_s=None,
            status="running",
            input=raw_input,
            output=None,
            error=None,
        )

        # 1) input validation
        try:
            validated_input = self.input_schema(**raw_input)
        except ValidationError as e:
            record.status = "error"
            record.error = f"InputvalidationError: {e}"
            record.end_ts = time.time()
            record.duration_s = record.end_ts - start_ts

            # Run on_error hooks
            self._run_hooks("on_error", record)

            return Agentoutput(output={}, confidence=0.0, metadata={"error": "input_validation"}), record

        # 2) before hooks
        self._run_hooks("before", record)

        # 3) Core execution (prepare + execute + finalize)
        try:
            self.prepare(validated_input, context)

            result_raw = self.execute(validated_input, context)

            if isinstance(result_raw, dict): # if the output is dict then convert dict to validated AgentOutput
                result = self.output_schema(**result_raw)
            elif isinstance(result_raw, Agentoutput): # if the output is already AgentOutput, use directly
                result = result_raw
            else:        
                result = self.output_schema(
                    **(
                        result_raw.dict() 
                        if hasattr(result_raw, "dict")  # if result_raw has a dict method, use same
                        else dict(result_raw)))  # else convert to dict and use 

            # finalize
            self.finalize(validated_input, result, context)

            record.status = "success"
            record.output = result.output
            record.end_ts = time.time()
            record.duration_s = record.end_ts - start_ts
            # after hooks
            self._run_hooks("after", record)
            return result, record

        except Exception as exc:
            record.status = "error"
            record.error = f"{type(exc).__name__}: {str(exc)}\n{traceback.format_exc()}"

            record.end_ts = time.time()
            record.duration_s = record.end_ts - start_ts

            # on_error hooks
            self._run_hooks("on_error", record)

            return (
                Agentoutput(
                    output={"error": str(exc)},
                    confidence=0.0,
                    metadata={"exception_type": type(exc).__name__},
                ),
                record,
            )
        
