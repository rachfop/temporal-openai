import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from your_activities import return_answer
from your_openai import OpenAIWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="open-ai-task-queue",
        workflows=[OpenAIWorkflow],
        activities=[return_answer],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
