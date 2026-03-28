# 🎓 Personalized Learning Path Agent — Documentation

## Overview

The **Personalized Learning Path Agent** is an AI-powered application that generates a customized learning curriculum and daily study plan based on a user's current skills and learning goals. It uses a LangGraph state machine to orchestrate a series of LLM-powered steps, and exposes a simple web interface via Gradio.

---

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

### Key Design Choices

- **Pydantic v1 (not v2):** LangChain's `.with_structured_output()` integration expects `pydantic.v1` models. Using native Pydantic v2 classes will cause compatibility errors.
- **GPT-4o-mini:** Chosen for cost-efficiency and speed. Can be swapped for `gpt-4o` for higher-quality output at greater cost.
- **LangGraph `StateGraph`:** Provides a clear, inspectable execution graph rather than a linear chain, making it easier to add conditional branching or parallel nodes in the future.
- **Gradio `Blocks` API:** Used instead of `gr.Interface` for more granular layout control over inputs, outputs, and the run button.

---

## Architecture

The agent is built on three core libraries:

| Library | Role |
|---|---|
| **LangGraph** | Orchestrates the multi-step agentic workflow as a directed state graph |
| **LangChain + OpenAI** | Powers each node with structured LLM calls (`gpt-4o-mini`) |
| **Gradio** | Provides the web-based user interface |

---

## Architectural View

The system is composed of three layers: a **UI layer** (Gradio), an **orchestration layer** (LangGraph state graph), and an **AI layer** (LangChain + OpenAI). User input flows top-down through each layer; results propagate back up to the interface.

```
┌──────────────────────────────────────────────────────┐
│                    UI Layer (Gradio)                  │
│   skills input │ goals input │ num_days │ Run button  │
│         summary out │ curriculum out │ plan out       │
└────────────────────────┬─────────────────────────────┘
                         │  run_agent()
                         ▼
┌──────────────────────────────────────────────────────┐
│           Orchestration Layer (LangGraph)             │
│                                                      │
│  LearningState (Pydantic model — shared across nodes)│
│                                                      │
│  ┌─────────────┐   ┌─────────────┐                  │
│  │ Assess      │──▶│ Decompose   │                  │
│  │ Skills      │   │ Goals       │                  │
│  └─────────────┘   └──────┬──────┘                  │
│                           │                          │
│  ┌─────────────┐   ┌──────▼──────┐                  │
│  │ Summarize   │◀──│ Create      │                  │
│  │ Progress    │   │ Weekly Plan │                  │
│  └─────────────┘   └─────────────┘                  │
│                                                      │
└────────────────────────┬─────────────────────────────┘
                         │  llm.with_structured_output()
                         ▼
┌──────────────────────────────────────────────────────┐
│                AI Layer (LangChain + OpenAI)          │
│                                                      │
│   ChatOpenAI (gpt-4o-mini, temperature=0.7)          │
│   Structured output schemas (Pydantic v1 models)     │
│     AssessSkillsOutput │ DecomposeGoalsOutput         │
│     CreateWeeklyPlanOutput │ SummarizeProgressOutput  │
└──────────────────────────────────────────────────────┘
```

### Data Flow Summary

1. The user provides skills, goals, and number of days in the Gradio UI.
2. `run_agent()` initialises a `LearningState` and invokes the compiled LangGraph chain.
3. Each graph node calls the LLM with a role-specific prompt, receives a typed structured output, and writes results back into the shared state.
4. After all four nodes complete, the final state is returned and the Gradio outputs are populated.

### Key Architectural Properties

- **Stateless between sessions** — `LearningState` is created fresh per invocation; nothing persists across runs.
- **Sequential, not parallel** — nodes execute one after another; each node depends on the output of the prior one.
- **Strongly typed at every boundary** — Pydantic models enforce schema at both the state level and the per-node LLM output level, catching hallucinated or malformed responses early.
- **Decoupled UI and logic** — the Gradio layer calls a single `run_agent()` function; the graph internals are fully independent of the UI framework.

---

## Workflow

The agent runs four sequential nodes, each calling the LLM with a specialized prompt:

```
Assess Skills → Decompose Goals → Create Weekly Plan → Summarize Progress
```

### 1. Assess Skills
- **Input:** `current_skills`, `learning_goals`
- **Output:** `summary` — a concise professional assessment of the user's strengths and gaps relative to their goals
- **LLM role:** Learning assessment specialist

### 2. Decompose Goals
- **Input:** `current_skills`, `learning_goals`, `summary`
- **Output:** `curriculum` — a numbered, ordered list of specific and measurable learning items
- **LLM role:** Curriculum designer

### 3. Create Weekly Plan
- **Input:** `curriculum`, `num_days`
- **Output:** `weekly_plan` — a day-by-day plan distributing curriculum items with time estimates
- **LLM role:** Learning planner

### 4. Summarize Progress
- **Input:** `user_name`, `weekly_plan`
- **Output:** Updated `summary` and `next_steps` — an achievement summary and actionable recommendations
- **LLM role:** Learning coach

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

## Known Limitations & Potential Improvements

| Issue | Suggested Fix |
|---|---|
| `next_steps` output not shown in UI | Add a fourth `gr.Textbox` output and wire it in `run_btn.click` |
| `user_name` is hardcoded to `"User"` | Add a name input field in Gradio and pass it through |
| No error handling for empty inputs | Add input validation before invoking the graph |
| No streaming — UI freezes during generation | Use `gr.Progress` or stream partial state updates |
| State is not persisted between sessions | Integrate a database or session store for multi-session support |

## Contribuer 
Biruk Geletu
Linkedin: https://www.linkedin.com/in/biruk-geletu/

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph).
- UI powered by [Gradio](https://www.gradio.app/)
