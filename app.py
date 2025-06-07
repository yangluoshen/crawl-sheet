from smolagents import MCPClient
from smolagents.gradio_ui import GradioUI
from agent import SmolCodeAgent, SmolCoderModelOpenrouter
from langfuse_trace import init_trace

def main():
    try:
        model = SmolCoderModelOpenrouter(
            # model_id="openai/gpt-4.1",
            # model_id="openai/gpt-4o-mini",
            # model_id="google/gemini-2.5-flash-preview-05-20",
            model_id="anthropic/claude-sonnet-4",
        )

        playwright_mcp = {
            "url": "http://localhost:8931/sse",
        }

        mcp_client = MCPClient([playwright_mcp])
        # browser_agent = ToolCallingAgent(model=model, tools=mcp_client.get_tools())
        # agent = SmolCodeAgent(model=model, tools=[], managed_agents=[browser_agent])
        tools = mcp_client.get_tools()
        agent = SmolCodeAgent(model=model, tools=tools)

        app = GradioUI(agent)
        app.launch()
    finally:
        if mcp_client:
            mcp_client.disconnect()


if __name__ == "__main__":
    init_trace()
    main()
