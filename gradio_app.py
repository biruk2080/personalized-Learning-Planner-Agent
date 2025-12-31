import gradio as gr
from PlannerAgent import LearningState, chain

def generate_plan(user_name, current_skills, learning_goals):
    current_skills_list = [skill.strip() for skill in current_skills.split(",")]
    learning_goals_list = [goal.strip() for goal in learning_goals.split(",")]
    
    initial_state = LearningState(
        user_name=user_name,
        current_skills=current_skills_list,
        learning_goals=learning_goals_list,
        curriculum=[],
        weekly_plan=[],
        next_steps=[]
    )
    
    final_state = chain.invoke(initial_state)
    
    curriculum_text = "\n".join(f"- {item}" for item in final_state['curriculum'])
    weekly_plan_text = "\n\n".join(final_state['weekly_plan'])
    next_steps_text = "\n".join(f"- {step}" for step in final_state['next_steps'])
    
    return curriculum_text, weekly_plan_text, next_steps_text

with gr.Blocks() as demo:
    gr.Markdown("# Personalized Learning Planner Chatbot")
    
    with gr.Row():
        user_name = gr.Textbox(label="Your Name", value="Alice")
        current_skills = gr.Textbox(label="Current Skills (comma-separated)", value="Python, HTML")
        learning_goals = gr.Textbox(label="Learning Goals (comma-separated)", value="Learn AI security, Master Data Structures")
    
    btn = gr.Button("Generate Plan")
    
    with gr.Column():
        curriculum = gr.Textbox(label="Curriculum", lines=10)
        weekly_plan = gr.Textbox(label="Weekly Plan", lines=20)
        next_steps = gr.Textbox(label="Next Steps", lines=5)
    
    btn.click(generate_plan, inputs=[user_name, current_skills, learning_goals], outputs=[curriculum, weekly_plan, next_steps])

if __name__ == "__main__":
    demo.launch()
