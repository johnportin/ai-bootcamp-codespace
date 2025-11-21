from pydantic import BaseModel


class GuardrailViolation(Exception):
    """Raised when a guardrail blocks the user's input."""

    def __init__(self, reasoning: str):
        super().__init__(reasoning)
        self.reasoning = reasoning


class EvidentlyDocsGuardrail(BaseModel):
    reasoning: str
    fail: bool


def input_guardrail(message: str) -> EvidentlyDocsGuardrail:
    """
    This function checks if the user message contains prohibited topics.
    Args:
        message: The user input message
    Returns:
        EvidentlyDocsGuardrail indicating if tripwire was triggered           
    """
    prohibited_topics = [
        "sqrt", "math", "history"
    ]

    for topic in prohibited_topics:
        if topic in message.lower():
            return EvidentlyDocsGuardrail(
                reasoning=f"Input contains prohibited topic: {topic}",
                fail=True,
            )

    return EvidentlyDocsGuardrail(
        reasoning="Input is clean",
        fail=False,
    )


def enforce_input_guardrail(message: str) -> EvidentlyDocsGuardrail:
    """
    Run the input guardrail and raise if the message is not allowed.
    """
    result = input_guardrail(message)
    if result.fail:
        raise GuardrailViolation(result.reasoning)
    return result
