from temporalio import activity
from dataclasses import dataclass
import openai
import os

# Define OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@dataclass
class OpenAIQuestion:
    answer: str


@activity.defn
async def return_answer(open_ai: OpenAIQuestion) -> str:
    activity.heartbeat(f"Heartbeating from {activity}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": f"{open_ai.answer}"},
        ],
    )

    result: str = ""
    for choice in response.choices:
        result += choice.message.content

    return result
