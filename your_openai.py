# your_openai.py
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from your_activities import OpenAIQuestion, return_answer


@workflow.defn
class OpenAIWorkflow:
    @workflow.run
    async def run(self, question: str) -> str:
        return await workflow.execute_activity(
            return_answer,
            OpenAIQuestion(question),
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                non_retryable_error_types=["WorkflowFailureError"],
            ),
        )
