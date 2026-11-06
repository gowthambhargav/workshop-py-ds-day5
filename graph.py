
from langgraph.graph import StateGraph, START, END

from state import InterviewState

from nodes import (
    analyze_answer,
    evaluate_answer,
    generate_feedback,
    generate_final_report
)


# Conditional routing function
def route_feedback(state: InterviewState):

    if state["score"] < 7:
        return "feedback"

    return "report"


# Create workflow
workflow = StateGraph(InterviewState)


# Add nodes
workflow.add_node("analyze", analyze_answer)
workflow.add_node("evaluate", evaluate_answer)
workflow.add_node("feedback", generate_feedback)
workflow.add_node("report", generate_final_report)


# Define workflow connections
workflow.add_edge(START, "analyze")

workflow.add_edge("analyze", "evaluate")

# Conditional routing
workflow.add_conditional_edges(
    "evaluate",
    route_feedback,
    {
        "feedback": "feedback",
        "report": "report"
    }
)

workflow.add_edge("feedback", "report")

workflow.add_edge("report", END)


# Compile workflow
app = workflow.compile()
