
from typing import TypedDict


class InterviewState(TypedDict):
    job_role: str
    question: str
    student_answer: str

    analysis: str
    score: int
    feedback: str

    final_report: str
