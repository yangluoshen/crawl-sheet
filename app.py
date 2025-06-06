from smolagents.gradio_ui import GradioUI
from agent import create_agent

agent = create_agent()

demo = GradioUI(agent)

if __name__ == "__main__":
    demo.launch()
