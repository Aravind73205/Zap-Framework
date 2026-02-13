# Zap - Multi Agent Orchestration Framework

##   Overview

Zap Framework is a modular multi-agent orchestration framework built from scratch to explore clean agent architecture, workflow orchestration, observability, memory persistence, and extensible AI systems.  The framework emphasizes transparency in how agents communicate, execute, and evolve across workflows.

It focuses on building clear execution flow and reusable orchestration patterns that make multi-agent pipelines understandable and easy to extend

The architecture keeps the orchestration engine lightweight and stable while allowing workflows, agents, and domain logic to be developed independently. This approach enables rapid experimentation, easier debugging, and a clear path toward integrating more advanced AI capabilities without redesigning the core system.

---

##  🚀 Core Concepts

- **Agents** → isolated logic units with strict input/output contracts
- **Orchestrator** → controls execution flow between agents
- **Workflow Steps** → define agent order and data transformation
- **Input Transformers (Adapters)** → safely map outputs to next agent inputs
- **Hooks** → logging, memory saving, guardrails
- **Memory Store** → persistent workflow history

---

## 🧠 Architecture Flow

```
User Input
↓
Orchestrator
↓
Workflow Steps
↓
Agents (validate → execute → output)
↓
Hooks (logging / memory / guardrails)
↓
Memory Store (JSON persistence)
```
---

## 📂 Project Structure

```
Zap-Framework/
├── app/
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
│       └── workflow/
│           └── marketing_workflow.py
│
├── engine/
│   ├── agent_base.py
│   ├── orchestrator.py
│   ├── hooks.py
│   ├── memory.py
│   └── guardrails.py
│
├── extensions/
│   ├── init.py
│   ├── logging_hook.py
│   ├── memory_hook.py
│   └── guardrail_hook.py
│
├── tests/
│   ├── test_agent_base.py
│   ├── test_orchestrator.py
│   ├── test_memory.py
│   └── test_marketing_workflow.py
│
├── .gitignore
├── LICENSE
└── README.md

```
---

##  Current Domain: Marketing Workflow

Phase 1 implements a deterministic marketing content pipeline:

1. **Input Validator Agent**  
   - Cleans and validates user input.

2. **Audience Analyzer Agent**  
   - Extracts structured audience insights (rule-based).

3. **Value Proposition Agent**  
   - Builds core message and key benefits.

4. **Content Outline Generator Agent**  
   - Produces final structured marketing outline.
     

Each agent output is transformed through workflow adapters before reaching the next agent.

---

## 🧪 This Executes

Running the workflow executes:

- orchestration pipeline  
- hooks lifecycle  
- memory persistence  
- structured execution records  

---

## 🔎 Hooks System

Hooks extend behavior without touching engine logic.

### Available Hooks:

#### 1) LoggingHook
- prints workflow lifecycle
- shows inputs & outputs

#### 2) MemoryHook
- saves runs into JSON storage

#### 3) GuardrailHook
- limits workflow steps
- validates required input keys
- blocks restricted agents


Hooks are optional and fully pluggable.

---

## 💾 Memory Persistence

Workflow runs are saved to: ( data/memory_store.json )

Each run stores:

- agent inputs
- outputs
- timestamps
- status
- metadata

This enables debugging and future learning-based improvements.

---

## 🎯 Design Goals

- Keep engine minimal and understandable
- Separate domain logic from core framework
- Allow plug-and-play agents
- Strong observability and debugging
- Easy evolution toward LLM-based agents

---

## 📈 Current Status

### ✅ Phase 1 — Deterministic Engine (Completed)

- Agent lifecycle system
- Orchestrator with workflow steps
- Adapter-based data passing
- Hook manager
- Guardrails
- Memory persistence
- Marketing domain workflow

---

## 🔜 Next Phase

Phase 2 introduces hybrid AI behavior:

- LLM-powered agents
- Hybrid deterministic + intelligent workflows
- Improved context handling
- Stronger error recovery

---

## ⚡ Why This Exists

Most frameworks hide orchestration internals.

Zap Framework is built to understand and control:

- how agents communicate
- how workflows execute
- where failures happen
- how memory evolves

The goal is not just using AI tools — but understanding how multi-agent systems actually work under the hood.

---
