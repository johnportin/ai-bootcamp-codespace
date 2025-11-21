from tools import (
    search_wikipedia_titles,
    SearchWikipediaTitlesArgs,
    get_wikipedia_page,
    GetWikipediaPageArgs
)
from wikiagent import wikipedia_agent
import asyncio
from wikiagent import NamedCallback
from wikiagent import wikipedia_agent

from agent_logging import (
    log_streamed_run,
    save_log
)

agent_callback = NamedCallback(wikipedia_agent)


async def run_agent(user_prompt: str):
    result = await wikipedia_agent.run(
        user_prompt=user_prompt,
        event_stream_handler=agent_callback
    )
    return result

result = asyncio.run(run_agent("Where do capybaras live?"))

# print(result.output)

# result = wikipedia_agent.run("Where do capybaras live?")

log_entry = await log_streamed_run(wikipedia_agent, result)
log_file = save_log(log_entry)
print(f"\n\nLog saved to: {log_file}")