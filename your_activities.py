from temporalio import activity
from dataclasses import dataclass
import openai
import os

# Define OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@dataclass
class OpenAIQuestion:
    question: str


@activity.defn
async def return_answer(open_ai: OpenAIQuestion) -> str:
    activity.heartbeat(f"Heartbeating from {activity.info().attempt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": f"{open_ai.question}"},
        ],
    )

    answer: str = ""
    for choice in response.choices:
        answer += choice.message.content

    return answer
