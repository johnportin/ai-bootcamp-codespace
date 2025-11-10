from main import run_agent
from tests.utils import get_tool_calls
import pytest
import re
import asyncio
from tests.judge import evaluate_agent_performance

question1 = "What are the three closest planets to Earth?"
question2 = "Who are the four Teenage Mutant Ninja Turtles?"
question3 = "What major citadel burnt down in Europe within the last 10 years?"
question4 = "What has the programming language Lean been used for?"
question5 = "What is one working definition for a ring to be Cohen-Macaulay?"
question6 = "Explain brownian motion to a 10 year old."
question7 = "What is the difference between inference and prediction?"
question8 = "Who are three influential mathematicians in the field of algebraic combinatorics active within the last 20 years?"
question9 = "What are the active business ventures of the Trump family?"
question10 = "Is the thumb considered a finger? Why or why not?"

questions = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10]

@pytest.mark.asyncio
async def test_ground_truth():
    print("Entered ground truth")
    for question in questions:
        print(f"Calling run agent for {question}")
        result = await run_agent(question)
        assert result.output
        text = result.output
        print(f"{question}\n\t {text}")