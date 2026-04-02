# 🎓 Personalized Learning Path Agent — Documentation

## Overview

The **Personalized Learning Path Agent** is an AI-powered application that generates a customized learning curriculum and daily study plan based on a user's current skills and learning goals. It uses prompt chain technque on LangGraph state machine to orchestrate a series of LLM-powered steps, and exposes a simple web interface via Gradio.

---
## Architectural View
The system is composed of three layers: a **UI layer** (Gradio), an **orchestration layer** (LangGraph state graph), and an **AI layer** (LangChain + OpenAI). User input flows top-down through each layer; results propagate back up to the interface.

![learning_agent_architecture](https://github.com/user-attachments/assets/3c3f3e0f-e8a0-432c-8fa0-ae34cb0ec411)
## Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **LLM** | OpenAI GPT-4o-mini | Latest | Natural language generation for all agent nodes |
| **LLM Integration** | LangChain (`langchain-openai`) | Latest | LLM client, structured output binding via `.with_structured_output()` |
| **Agent Orchestration** | LangGraph | Latest | Directed state graph — manages node sequencing and shared state |
| **Data Validation** | Pydantic v1 | v1 (via `pydantic.v1`) | State schema and per-node output schemas with type enforcement |
| **UI Framework** | Gradio | Latest | Browser-based web interface for user inputs and displaying results |
| **Configuration** | python-dotenv | Latest | Loads `OPENAI_API_KEY` from `.env` file at runtime |
| **Language** | Python | 3.9+ | Application runtime |

---

The agent is built on three core libraries:

| Library | Role |
|---|---|
| **LangGraph** | Orchestrates the multi-step agentic workflow as a directed state graph |
| **LangChain + OpenAI** | Powers each node with structured LLM calls (`gpt-4o-mini`) |
| **Gradio** | Provides the web-based user interface |

---

## Workflow

The agent runs four sequential nodes, each calling the LLM with a specialized prompt:

```
Assess Skills → Decompose Goals → Create Weekly Plan → Summarize Progress
```

---

## State Schema

All data flows through a shared `LearningState` Pydantic model:

| Field | Type | Description |
|---|---|---|
| `user_name` | `str` | The learner's name |
| `current_skills` | `List[str]` | Skills the user already has |
| `learning_goals` | `List[str]` | What the user wants to learn |
| `curriculum` | `List[str]` | Generated curriculum items (populated by node 2) |
| `weekly_plan` | `List[str]` | Day-by-day plan entries (populated by node 3) |
| `next_steps` | `List[str]` | Post-plan recommendations (populated by node 4) |
| `num_days` | `int` | Number of days to plan for |
| `summary` | `str` | Skills assessment or progress summary (updated by nodes 1 and 4) |

---

## Output Schemas

Each node uses a dedicated Pydantic model for structured LLM output, ensuring type safety:

| Schema | Fields |
|---|---|
| `AssessSkillsOutput` | `summary: str` |
| `DecomposeGoalsOutput` | `curriculum: List[str]` |
| `CreateWeeklyPlanOutput` | `weekly_plan: List[str]` |
| `SummarizeProgressOutput` | `summary: str`, `next_steps: List[str]` |

---

## User Interface

The Gradio UI exposes three inputs and three outputs:

**Inputs:**

| Field | Type | Example |
|---|---|---|
| Current Skills | Text (comma-separated) | `Python, HTML, SQL` |
| Learning Goals | Text | `Build a full-stack web app` |
| Number of Days | Number | `7` |

**Outputs:**

| Field | Description |
|---|---|
| 📊 Skills Assessment Summary | LLM-generated profile of strengths and gaps |
| 📘 Curriculum | Ordered list of learning steps |
| 📅 Plan | Day-by-day study schedule |

> **Note:** The `next_steps` output is computed by the graph but is not currently wired to a Gradio output component.

---

## Setup & Installation

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Install Dependencies

```bash
pip install langchain langchain-openai langgraph pydantic gradio python-dotenv
```

### Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### Run the Application

```bash
python app.py
```

The Gradio interface will launch locally and print a public shareable link (via `share=True`).

---

## Configuration

### Changing the LLM

The model is initialized at the top of the file. To switch models or adjust creativity:

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Change to "gpt-4o" for higher quality
    temperature=0.7        # Lower for more deterministic output
)
```

### Adjusting Prompts

Each node function contains its own prompt string. To customize the agent's behavior (e.g., focus on a specific domain like coding or language learning), edit the prompt text inside the relevant node function (`assess_skills`, `decompose_goals`, etc.).

---

## Contribuer 
Biruk Geletu
Linkedin: https://www.linkedin.com/in/biruk-geletu/

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph).
- UI powered by [Gradio](https://www.gradio.app/)
