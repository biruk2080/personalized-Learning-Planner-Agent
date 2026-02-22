from typing import TypedDict, List
from pydantic.v1 import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()
import gradio as gr

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)
# Define the State Schema
class LearningState(BaseModel):
    user_name: str
    current_skills: List[str]
    learning_goals: List[str]
    curriculum: List[str]
    weekly_plan: List[str]
    next_steps: List[str]
    num_days: int
    summary: str
  

# Define Output Schemas
class AssessSkillsOutput(BaseModel):
    summary: str

class DecomposeGoalsOutput(BaseModel):
    curriculum: List[str]

class CreateWeeklyPlanOutput(BaseModel):
    weekly_plan: List[str]

class SummarizeProgressOutput(BaseModel):
    summary: str
    next_steps: List[str]

# Define Node Functions
def assess_skills(state: LearningState) -> LearningState:
    """Ask LLM to analyze user skills and produce structured skill profile"""
    prompt = f"""
    You are a professional learning assessment specialist. Analyze the following:
    
    Current Skills: {', '.join(state.current_skills)}
    Learning Goals: {', '.join(state.learning_goals)}
    
    Provide a concise summary of the user's strengths and weaknesses relevant to achieving their learning goals.
    Format your response as a professional assessment summary.
    """
    llm_structured = llm.with_structured_output(AssessSkillsOutput)
    response = llm_structured.invoke(prompt)
    state.summary = response.summary
    return state

def decompose_goals(state: LearningState) -> LearningState:
    """Break learning goals into actionable curriculum items"""
    prompt = f"""
    You are a professional curriculum designer specialized in creating personalized learning paths.
    
    Current Skills: {', '.join(state.current_skills)}
    Learning Goals: {', '.join(state.learning_goals)}
    Skills Assessment: {state.summary}
    
    Break down these learning goals into a step-by-step actionable curriculum. Each curriculum item should be:
    - Specific and measurable
    - Logically ordered for progressive learning
    - Realistic to complete
    
    Return a numbered list of curriculum items.
    """
    llm_structured = llm.with_structured_output(DecomposeGoalsOutput)
    response = llm_structured.invoke(prompt)
    state.curriculum = response.curriculum
    return state

def create_weekly_plan(state: LearningState) -> LearningState:
    """Generate a weekly learning plan based on curriculum"""
    prompt = f"""
    You are an expert learning planner. Create a detailed {state.num_days}-day learning plan.
    
    Curriculum to cover: {', '.join(state.curriculum)}
    
    Requirements:
    - Distribute all curriculum items across {state.num_days} days
    - Each daily plan should have specific, actionable tasks
    - Include estimated time for each task
    - Ensure progressive difficulty and logical sequencing
    - Do not add items outside the provided curriculum
    
    Return each day's plan in a clear, organized format with tasks and time estimates.
    """
    llm_structured = llm.with_structured_output(CreateWeeklyPlanOutput)
    response = llm_structured.invoke(prompt)
    state.weekly_plan = response.weekly_plan
    return state

def summarize_progress(state: LearningState) -> LearningState:
    """Summarize learning progress and suggest next steps"""
    prompt = f"""
    You are a learning coach providing progress feedback.
    
    User: {state.user_name}
    Completed Weekly Plan: {', '.join(state.weekly_plan)}
    
    Provide:
    1. A concise summary of learning progress and key achievements
    2. Specific next steps for continued learning
    
    Format the next steps as a numbered list of actionable recommendations.
    """
    llm_structured = llm.with_structured_output(SummarizeProgressOutput)
    response = llm_structured.invoke(prompt)
    state.next_steps = response.next_steps
    state.summary = response.summary
    return state

# Build the State Graph

learning_graph = StateGraph(LearningState)
learning_graph.add_node("Assess Skills", assess_skills)
learning_graph.add_node("Decompose Goals", decompose_goals)
learning_graph.add_node("Create Weekly Plan", create_weekly_plan)
learning_graph.add_node("Summarize Progress", summarize_progress)

learning_graph.add_edge("Assess Skills", "Decompose Goals")
learning_graph.add_edge("Decompose Goals", "Create Weekly Plan")
learning_graph.add_edge("Create Weekly Plan", "Summarize Progress") 

learning_graph.set_entry_point("Assess Skills")
chain = learning_graph.compile()

# Gradio Interface agent call 

def run_agent(skills, goals, num_days):
    state = LearningState(
        user_name="User",
        current_skills=[s.strip() for s in skills.split(",") if s.strip()],
        learning_goals=[g.strip() for g in goals.split(",") if g.strip()],
        curriculum=[],
        weekly_plan=[], 
        next_steps=[],
        num_days=num_days,
        summary=""
    )

    final_state = chain.invoke(state)

    return (
        final_state["summary"],
        "\n".join(final_state["curriculum"]),
        "\n".join(final_state["weekly_plan"]),
        "\n".join(final_state["next_steps"]),
    )

# Gradio UI


with gr.Blocks(title="Personalized Learning Path Agent") as demo:
    gr.Markdown("## 🎓 Personalized Learning Path Agent")

    skills = gr.Textbox(
        label="Current Skills (comma separated)",
        placeholder="Python, HTML, SQL"
    )
    goals = gr.Textbox(
        label="Learning Goals",
        placeholder="put your learning goals here"
    )
    num_days = gr.Number(label="Number of Days", value=7)

    run_btn = gr.Button("Generate Learning Plan")

    summary_out = gr.Textbox(
        label="📊 Skills Assessment Summary",
        lines=4
    )
    curriculum_out = gr.Textbox(
        label="📘 Curriculum",
        lines=6
    )
    weekly_plan_out = gr.Textbox(
        label="📅 Plan",
        lines=6
    )


    run_btn.click(
        fn=run_agent,
        inputs=[skills, goals, num_days],
        outputs=[summary_out, curriculum_out, weekly_plan_out],
    )

demo.launch(share= True)
