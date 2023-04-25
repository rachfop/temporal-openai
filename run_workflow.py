from flask import Flask, render_template, request
from temporalio.client import Client
from your_openai import OpenAIWorkflow

app = Flask(__name__)

# List to store the chat history
chat_history = []


@app.route("/")
def display_form():
    return render_template("index.html")


@app.route("/answer", methods=["POST"])
async def open_ai_answer():
    user_question = f'{request.form.get("question")}'

    client = await Client.connect("localhost:7233")

    answer = await client.execute_workflow(
        OpenAIWorkflow.run,
        user_question,
        id=user_question.replace(" ", "-").lower(),
        task_queue="open-ai-task-queue",
    )

    # Add the user's question and answer to the chat history
    chat_history.append({"question": user_question, "answer": answer})

    return render_template(
        "index.html", question=user_question, answer=answer, chat_history=chat_history
    )


if __name__ == "__main__":
    app.run(debug=True)
