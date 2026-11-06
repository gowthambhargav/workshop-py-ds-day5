import os
from dotenv import load_dotenv
from typing import TypedDict

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END

load_dotenv()

model = ChatOpenRouter(
    model=os.environ["MODEL_NAME"],
)


class State(TypedDict):
    topic: str
    explanation: str
    example: str
    final: str


def text_content(response) -> str:
    content = response.content
    if isinstance(content, list):
        return "\n".join(
            part.get("text", str(part)) if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)


def explain_topic(state: State) -> dict[str, str]:
    response = model.invoke(
        f"Explain {state['topic']} clearly for a beginner in a few paragraphs."
    )
    return {"explanation": text_content(response)}


def create_example(state: State) -> dict[str, str]:
    response = model.invoke(
        f"Give one practical, easy-to-understand example of {state['topic']}."
    )
    return {"example": text_content(response)}


def finalize(state: State) -> dict[str, str]:
    return {
        "final": (
            f"Topic: {state['topic']}\n\n"
            f"Explanation:\n{state['explanation']}\n\n"
            f"Example:\n{state['example']}"
        )
    }


builder = StateGraph(State)
builder.add_node("explain_topic", explain_topic)
builder.add_node("create_example", create_example)
builder.add_node("finalize", finalize)

builder.add_edge(START, "explain_topic")
builder.add_edge("explain_topic", "create_example")
builder.add_edge("create_example", "finalize")
builder.add_edge("finalize", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "topic": "deep learning",
            "explanation": "",
            "example": "",
            "final": "",
        }
    )
    print(result["final"])
