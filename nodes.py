
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import json
import re

load_dotenv()


# Initialize OpenRouter LLM
llm = ChatOpenRouter(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=2000
)


# Generate interview question
def generate_interview_question(job_role):

    prompt = f"""
    You are an experienced technical interviewer.

    Generate ONE interview question for the following job role:

    Job Role: {job_role}

    Requirements:
    1. Generate a practical interview question.
    2. Keep it suitable for students preparing for placements.
    3. Avoid extremely advanced questions.
    4. Return only the interview question.
    """

    response = llm.invoke(prompt)

    return response.content.strip()


# Node 1: Analyze interview answer
def analyze_answer(state):

    prompt = f"""
    You are an experienced technical interviewer.

    Job Role: {state['job_role']}
    Interview Question: {state['question']}
    Student Answer: {state['student_answer']}

    Analyze the student's answer based on:

    1. Technical correctness
    2. Relevance
    3. Clarity
    4. Completeness

    Provide a simple and concise analysis.
    """

    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }


# Node 2: Evaluate interview answer
def evaluate_answer(state):

    prompt = f"""
    You are an interview evaluator.

    Evaluate the following answer.

    Job Role: {state['job_role']}
    Question: {state['question']}
    Student Answer: {state['student_answer']}

    Analysis:
    {state['analysis']}

    Use this evaluation rubric:

    Technical correctness: 0-4 marks
    Relevance: 0-2 marks
    Clarity: 0-2 marks
    Completeness: 0-2 marks

    Return ONLY a valid JSON object:

    {{
        "score": 7
    }}

    The score must be an integer between 0 and 10.
    """

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()
        match = re.search(r'\{.*?\}', content, re.DOTALL)

        if not match:
            raise ValueError("Score JSON not found")

        data = json.loads(match.group())
        score = int(data["score"])

        if not 0 <= score <= 10:
            raise ValueError("Score must be between 0 and 10")

    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as e:
        raise ValueError(
            f"Could not extract a valid score: {response.content}"
        ) from e

    return {
        "score": score
    }


# Node 3: Generate improvement feedback
def generate_feedback(state):

    prompt = f"""
    You are a professional placement interview coach.

    Job Role: {state['job_role']}
    Question: {state['question']}
    Student Answer: {state['student_answer']}

    Analysis:
    {state['analysis']}

    Score: {state['score']}/10

    Generate constructive feedback.

    Include:

    1. What was good?
    2. What needs improvement?
    3. Three specific improvement suggestions.
    4. A sample improved answer.

    Use simple language.
    """

    response = llm.invoke(prompt)

    return {
        "feedback": response.content
    }


# Node 4: Generate final evaluation report
def generate_final_report(state):

    feedback = state.get("feedback") or (
        "The answer met the evaluation threshold. "
        "Additional improvement feedback was not required."
    )

    prompt = f"""
    Create a professional interview evaluation report.

    Job Role: {state['job_role']}
    Question: {state['question']}
    Student Answer: {state['student_answer']}

    Analysis:
    {state['analysis']}

    Score: {state['score']}/10

    Feedback:
    {feedback}

    Generate a report containing:

    1. Job Role
    2. Interview Question
    3. Evaluation Score
    4. Answer Analysis
    5. Improvement Feedback
    6. Final Recommendation

    Keep the report professional and easy to understand.
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }
