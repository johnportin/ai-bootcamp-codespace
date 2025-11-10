from pydantic_ai import Agent
from tools import (
    search_wikipedia_titles,
    get_wikipedia_page,
    SearchWikipediaTitlesArgs,
    GetWikipediaPageArgs
)
import os
from dotenv import load_dotenv
from pydantic_ai.messages import FunctionToolCallEvent

load_dotenv()

print("Loaded API key:", "FOUND" if os.getenv("OPENAI_API_KEY") else "MISSING")

class NamedCallback:

    def __init__(self, agent):
        self.agent_name = agent.name

    async def print_function_calls(self, ctx, event):
        # Detect nested streams
        if hasattr(event, "__aiter__"):
            async for sub in event:
                await self.print_function_calls(ctx, sub)
            return

        if isinstance(event, FunctionToolCallEvent):
            tool_name = event.part.tool_name
            args = event.part.args
            print(f"TOOL CALL ({self.agent_name}): {tool_name}({args})")

    async def __call__(self, ctx, event):
        return await self.print_function_calls(ctx, event)


instructions="""
You are a Wikipedia research assistant. ALWAYS use the tools to gather information.

Workflow:
1. Use search_wikipedia_titles(query) to find relevant candidate pages.
2. Select the single most relevant title.
3. Use get_wikipedia_page(title) to fetch the summary.
4. Summarize clearly in under 500 words. 

Always cite the url in the repsonse. Do not use emojis.
"""

wikipedia_agent = Agent(
    name="Wiki",
    model="openai:gpt-4o-mini",
    instructions=instructions,
    tools=[
        search_wikipedia_titles,
        get_wikipedia_page
    ]
)