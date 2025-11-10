from tools import (
    search_wikipedia_titles,
    SearchWikipediaTitlesArgs,
    get_wikipedia_page,
    GetWikipediaPageArgs
)
from wikiagent import wikipedia_agent
import asyncio
from wikiagent import NamedCallback

agent_callback = NamedCallback(wikipedia_agent)


async def run_agent(user_prompt: str):
    result = await wikipedia_agent.run(
        user_prompt=user_prompt,
        event_stream_handler=agent_callback
    )
    return result

result = asyncio.run(run_agent("Where do capybaras live?"))

print(result.output)