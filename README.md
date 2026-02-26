# Zap - Multi Agent Orchestration Framework

## 🎄 Overview

Zap is a modular multi-agent orchestration framework built from scratch to explore clean architecture for multi-agent AI systems.

The framework focuses on:
   - Clear execution flow
   - Strict input/output contracts
   - LLM provider abstraction
   - Retry handling via wrappers
   - Execution hooks

Zap keeps the orchestration engine minimal while allowing agents, workflows, and LLM providers to evolve independently.

---

##  ⚜️ Core Concepts

- **Agents** → Isolated logic units with strict input/output contracts
- **Orchestrator** → Controls execution flow between agents
- **Workflow Steps** → Define agent order and data transformation
- **Input Transformers** → Safely map outputs to next agent inputs
- **LLM Abstraction Layer** → Use any language model without changing the code.
- **Retry Wrapper** → Retry logic for LLM calls
- **Hooks** → Logging, memory saving, guardrails
- **Memory Store** → Persistent JSON workflow history

---

## 🧠 Architecture Flow

```
User Input(CLI)
    ↓
Orchestrator
    ↓
Workflow Steps
    ↓
Agents 
    ↓
RetryLLM
    ↓
GeminiClient (LLM Provider)
    ↓
External API
```
---

## ✅ How To Run

**1. Clone the repository**

   ```
   git clone https://github.com/Aravind73205/zap-framework.
   cd zap-framework
   ```

**2. Install dependencies**

   ```
   pip install -r requirements.txt
   ```

**3. Set up environment variables**

- Open `.env` and add your actual key:
  
```
GEMINI_API_KEY = ypur Gemini API Key here
```

**4. Run the marketing workflow demo**
  ```
  python run_marketing.py
  ```

---

## 📂 Project Structure

```
Zap-Framework/
│
├── data/
│   └── memory_store.json
│
├── domains/
│   └── marketing/
│       ├── agents/
│       │   ├── input_validator_agent.py
│       │   ├── audience_analyzer_agent.py
│       │   ├── value_proposition_agent.py
│       │   └── content_outline_generator.py
│       │
│       ├── workflow/
│       │   └── marketing_workflow.py
│       │
│       └── agent_factory.py
│
├── engine/
│   ├── agent_base.py
│   ├── orchestrator.py
│   ├── hooks.py
│   ├── memory.py
│   ├── guardrails.py
│   └── config.py
│
├── extensions/
│   ├── llm/
│   │   ├── base.py
│   │   ├── gemini.py
│   │   └── retry_wrapper.py
│   ├── hooks
│       ├── logging_hook.py
│       ├── memory_hook.py
│       └── guardrail_hook.py         
│
├── tests/
│   ├── test_agent_base.py
│   ├── test_orchestrator.py
│   ├── test_memory.py
│   └── test_marketing_workflow.py
│
├── run_marketing.py
├── .gitignore
├── LICENSE
└── README.md

```
---

##  🧩 LLM Architecture

Zap uses a provider-agnostic LLM design.

**BaseLLM** (Contract):
   ```
    generate_json(prompt: str) -> Dict[str, Any]
   ```
All providers must implement this.

---

## 🔁 RetryLLM:

RetryLLM wraps any BaseLLM implementation.

Responsibilities:

   - Retry failed LLM calls
   - Log retry attempts
   - Raise final error if all retries fail

Agents never know retry logic exists.
GeminiClient never knows retry logic exists.

This separation follows the decorator pattern.

---

## 🏭 Agent Factory

Agents are constructed via `agent_factory.py.`

Responsibilities:

   - Instantiate LLM provider
   - Wrap provider with RetryLLM
   - Inject LLM into LLM-based agents
   - Keep agents provider-agnostic

This prevents tight coupling between agents and specific LLM implementations.

---

## 🔖 Hooks System

Hooks extend behavior without touching engine logic.

#### 1) LoggingHook
- Logs workflow lifecycle
- Displays agent inputs and outputs
- Shows status and duration

#### 2) MemoryHook
- Persists agent execution records
- Saves structured data to `data/memory_store.json`

#### 3) GuardrailHook
- Validates required inputs
- Limits workflow steps
- Blocks restricted agents
- Raises `GuardrailViolation` to stop execution safely

Hooks are optional and fully pluggable.

---

## 💾 Memory Persistence

All agent runs are stored in:

   `data/memory_store.json`

Each record includes:

   - run_id
   - agent_name
   - input
   - output
   - status
   - error (if any)
   - duration
   - metadata

This enables:

   - Debugging
   - Auditing
   - Future learning systems
   - Replay capability
     
---

## ♾️ Current Domain: Marketing Workflow

Implemented agents:

   1) Input Validator (rule-based)
   2) Audience Analyzer (LLM-based)
   3) Value Proposition Generator (LLM-based)
   4) Content Outline Generator (LLM-based)

Workflow is deterministic in structure but hybrid in intelligence.

---

## 🔮 Upcoming Enhancements

Zap is designed to evolve toward production-grade multi-agent orchestration. Planned upgrades include:

   1) Async Orchestrator - eliminate idle network wait time   
   2) Parallel Agent Execution - reduce overall latency      
   3) Token & Cost Tracking - for cost transparency      
   4) Streaming Support - improve user experience for long running agent tasks

---

## 🎯 Design Goals

- Keep engine minimal and understandable
- Separate domain logic from core framework
- Allow plug-and-play agents
- Strong observability and debugging

---

## 🧠 Design Philosophy

Zap is built to understand and control:

   - How agents communicate
   - How workflows execute
   - Where failures occur
   - How retry logic behaves
   - How memory evolves over time

The goal is not just to use AI APIs — but to understand how multi-agent systems function under the hood.