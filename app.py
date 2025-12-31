import streamlit as st
from PlannerAgent import LearningState, learning_graph, chain

st.title("Personalized Learning Planner Chatbot")

st.header("Enter Your Details")
user_name = st.text_input("Your Name", "Alice")
current_skills = st.text_area("Current Skills (comma-separated)", "Python, HTML").split(", ")
learning_goals = st.text_area("Learning Goals (comma-separated)", "Learn AI security, Master Data Structures").split(", ")

if st.button("Generate Plan"):
    initial_state = LearningState(
        user_name=user_name,
        current_skills=current_skills,
        learning_goals=learning_goals,
        curriculum=[],
        weekly_plan=[],
        next_steps=[]
    )
    
    final_state = chain.invoke(initial_state)
    
    st.header("Personalized Learning Plan")
    
    st.subheader("Curriculum")
    for item in final_state['curriculum']:
        st.write(f"- {item}")
    
    st.subheader("Weekly Plan")
    for week in final_state['weekly_plan']:
        st.write(week)
        st.write("")
    
    st.subheader("Next Steps")
    for step in final_state['next_steps']:
        st.write(f"- {step}")
