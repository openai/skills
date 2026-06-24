---
name: meshflow
description: Build, run, orchestrate, govern, debug, or optimize multi-agent workflows, agentic pipelines, and LLM-powered systems. Use when the user wants to build agents, form agent teams, add compliance (HIPAA/SOC2/GDPR), apply cost caps, add guardrails, create durable workflows, add human-in-the-loop checkpoints, wrap LangGraph/CrewAI/AutoGen with governance, reduce token costs, or ship agents to production safely.
---

# MeshFlow — Production-Safe Multi-Agent Orchestration

MeshFlow is the infrastructure layer for production agent deployments.
Compliant, cost-governed, and durable — out of the box, not bolted on.

```python
from meshflow import Workflow, CostCap, Agent

wf = Workflow(cost_cap=CostCap(usd=5.00))
wf.add(Agent('researcher'), Agent('analyst'), Agent('writer'))
result = wf.run('Write a competitive analysis of our market')
# Compliant. Durable. Audited. Cost-capped.
```

```bash
pip install meshflow
```

## Core patterns

### Build an agent

```python
from meshflow import Agent, tool, RiskTier

@tool(name="web_search", risk=RiskTier.EXTERNAL_IO)
async def web_search(query: str) -> str:
    return results

agent = Agent(
    name="researcher",
    role="researcher",
    model="claude-sonnet-4-6",  # or "gpt-4o", "llama3.2"
    tools=[web_search],
    memory=True,
)
result = await agent.run("Research the topic")
```

### Agent team

```python
from meshflow import Agent, Team

team = Team(
    [Agent("planner", role="planner"), Agent("coder", role="executor")],
    pattern="supervised",  # or: sequential, parallel, hierarchical
)
result = await team.run("Build a REST API")
```

### Compliance (HIPAA / SOC2 / GDPR)

```python
from meshflow import Agent, compliance_profile

agent = Agent(
    name="clinical",
    role="executor",
    policy=compliance_profile("hipaa"),  # sox, gdpr, pci, nerc
)
```

### Cost cap + token optimization

```python
from meshflow import Workflow, CostCap, ModelRouter

wf = Workflow(cost_cap=CostCap(usd=5.00))  # stops before $5
agent = Agent(name="a", model_router=ModelRouter())  # routes cheap tasks to smaller models
```

### Durable execution (crash recovery)

```python
from meshflow import DurableWorkflowExecutor

exe = DurableWorkflowExecutor(run_id="my-run", backend="redis")
# Same run_id on restart = resume from last checkpoint
```

### Human-in-the-loop

```python
from meshflow import StateGraph, interrupt

def approval_step(state):
    decision = interrupt("Approve this action?")
    return {"approved": decision.approved}
```

### Wrap existing LangGraph / CrewAI / AutoGen

```python
from meshflow import govern, from_langgraph, from_crewai

governed = govern(your_existing_app)       # any framework
governed = from_langgraph(your_graph)      # LangGraph
governed = from_crewai(your_crew)          # CrewAI
```

### Sandbox (no API key needed)

```python
wf = Workflow(mode="sandbox")  # zero real tokens, full trace
result = wf.run("test task")
```

## What every run gets automatically

- SHA-256 tamper-evident audit chain
- Hard cost cap enforcement
- HIPAA/SOX/GDPR compliance profiles
- Crash recovery (SQLite/Redis/Postgres/S3)
- 70-85% token cost reduction
- Rate limiting and SLA tracking

## Links

- GitHub: https://github.com/Anteneh-T-Tessema/meshflow
- Docs: https://meshflow.dev
- PyPI: https://pypi.org/project/meshflow/
