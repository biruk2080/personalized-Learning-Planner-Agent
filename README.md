# Personalized Learning Planner Agent

This demo showcases a sophisticated AI-powered learning assistant that generates personalized learning plans based on a user’s current skills, learning goals, and available time.

Built with LangChain, LangGraph, and use Huggingface Gradio UI and space to deploy and serve, the system demonstrates how modern LLM workflows can be orchestrated into a modular, state-driven AI agent with an interactive web interface.

## Features

- Skills Assessment: Analyzes user skills and provides a summary of strengths and weaknesses.
- Curriculum Generation: Breaks down learning goals into actionable curriculum items.
- Customizable Plans: Generates learning plans for a specified number of days.
- Interactive UI: Web-based interface using Gradio for easy interaction.
- Modular Architecture: Uses LangGraph for state management and workflow orchestration.

## Requirements

- Python 3.8+
- OpenAI API Key (for LLM interactions)
- LangGraph and LangChain 
- HuggingFace Gradio and space server 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/personalized-learning-planner.git
   cd personalized-learning-planner
   ```

2. Install dependencies:
   ```bash
   pip install langchain-openai langgraph pydantic gradio python-dotenv
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python PlannerAgent.py
   ```

2. Open the provided Gradio URL in your browser (usually `http://127.0.0.1:7860`).

3. Input your current skills, learning goals, and the number of days for the plan.

4. Click "Generate Learning Plan" to receive a personalized plan.

## Project Structure

- `PlannerAgent.py`: Main application file containing the LangGraph workflow and Gradio UI.
- `README.md`: This file.
- `.env`: Environment variables (not included in repo).

## How It Works

The agent uses a state graph with the following nodes:
1. Assess Skills: Evaluates user skills and goals to provide a summary.
2. Decompose Goals: Creates a step-by-step curriculum.
3. Create Plan: Generates a detailed daily learning plan.
4. Summarize Progress: Suggests next steps.

Each node leverages OpenAI's GPT model for intelligent content generation.

## Contribuer 
Biruk Geletu
Linkedin: https://www.linkedin.com/in/biruk-geletu/

## License
This project is built for learing purpose to demonstrate the capability of LangGraph to build complex task. 

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph).
- UI powered by [Gradio](https://www.gradio.app/).# personalized-Learning-Planner-Agent
# YouTub Demo Video Link 
https://youtu.be/XDGwAoDcjxY
