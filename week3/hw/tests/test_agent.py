from main import run_agent
from tests.utils import get_tool_calls
import pytest
import re
import asyncio
from tests.judge import evaluate_agent_performance


@pytest.mark.asyncio
async def test_agent_tool_calls_present_async():
    result = await run_agent("LLM as a Judge")
    assert result.output
    print(result.output)

    tool_calls = get_tool_calls(result)
    assert len(tool_calls) > 0, "No tool calls found"

@pytest.mark.asyncio
async def test_agent_includes_webpage_in_output():
    result = await run_agent("Where do capybaras live?")
    assert result.output

    pattern = r'https?://\S+|www\.\S+'
    has_webpage = re.findall(pattern, result.output)
    assert len(has_webpage) > 0

@pytest.mark.asyncio
async def test_no_judicial_terms_in_search_queries():
    criteria = [
        "agent makes at least 3 search calls",
        "the references are relevant to the topic",
        "each section has references",
        "all search queries are free of judicial terms (except 'judge')",
        "the article contains properly formatted python code examples",
    ]

    result = await run_agent("what is llm as a judge evaluation")

    eval_results = await evaluate_agent_performance(
        criteria,
        result,
        # output_transformer=lambda x: x.format_article()
        output_transformer=None
    )

    print(eval_results)

    for criterion in eval_results.criteria:
        print(criterion)
        assert criterion.passed, f"Criterion failed: {criterion.criterion_description}"
