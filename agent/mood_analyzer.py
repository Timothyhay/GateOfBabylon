from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal

from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace

"""

"""


@dataclass
class EvaluationFeedback:
    feedback: str
    summary_word: str
    score: float


evaluator = Agent[None](
    name="evaluator",
    instructions=(
        "You evaluate a diary about a day in weekend. "
        "You need to give a float score to describe the happiness. "
        "10.0 represents the most positive sentiment, and 0.0 for the opposite."
        "Then use a single word to summary sentiment or experience of this day."
    ),
    output_type=EvaluationFeedback,
)


async def main() -> None:
    # @TODO connect from notion data pool
    records = []
    msg = ""
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    # We'll run the entire workflow in a single trace
    with trace("Sentiment Analyzer"):
        for record in records:

            evaluator_result = await Runner.run(evaluator, input_items)
            result: EvaluationFeedback = evaluator_result.final_output

            print(f"Evaluator score: {result.score}")

            # @TODO: Append comments

    print(f"Final story outline: {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())
