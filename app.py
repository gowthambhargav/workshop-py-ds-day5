
import streamlit as st
from graph import app as workflow_app
from nodes import generate_interview_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PlacementAI | Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "generated_question_input": "",
    "generated_for_role": "",
    "custom_question": "",
    "result": None,
    "total_attempts": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F5F7FB;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Header */
.hero {
    background: linear-gradient(120deg, #172554, #1D4ED8);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #DBEAFE;
    font-size: 15px;
    margin-bottom: 0;
}

/* Section headings */
.section-heading {
    font-size: 21px;
    font-weight: 750;
    color: #172554;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 14px;
    border-color: #E2E8F0;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    min-height: 43px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: #2563EB;
    border: none;
    color: white;
}

/* Inputs */
.stTextArea textarea {
    border-radius: 9px;
    background-color: #FFFFFF;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 9px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 17px;
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🎯 PlacementAI")
    st.caption("Your personal AI interview coach")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Interview Practice",
            "📊 My Evaluation",
            "ℹ️ About Project"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ⚙️ Application Settings")

    st.caption("AI Model")
    st.success("GPT-OSS via OpenRouter")

    st.caption("Workflow Engine")
    st.info("LangGraph")

    st.caption("Monitoring")
    st.info("LangSmith")

    st.divider()

    st.metric(
        "Completed Evaluations",
        st.session_state.total_attempts
    )

    if st.button("🗑️ Reset Application", use_container_width=True):

        for key in defaults:
            if key == "total_attempts":
                st.session_state[key] = 0
            else:
                st.session_state[key] = defaults[key]

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <h1>AI Placement Feedback Assistant</h1>
    <p>
        Practice technical interviews, evaluate your answers,
        discover improvement areas and become placement ready.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INTERVIEW PRACTICE PAGE
# ============================================================

if page == "🏠 Interview Practice":

    st.markdown(
        '<div class="section-heading">🚀 Start Your Interview Practice</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose your target job role and practise answering "
        "realistic interview questions."
    )

    # --------------------------------------------------------
    # JOB ROLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 1. Select Your Career Role")

        job_role = st.selectbox(
            "Target Job Role",
            [
                "Python Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "Full Stack Developer",
                "AI Engineer",
                "Software Developer",
                "Data Analyst",
                "Cloud Engineer"
            ],
            key="job_role"
        )

        st.caption(
            "Your interview question and evaluation will be based on this role."
        )

    # --------------------------------------------------------
    # QUESTION GENERATION
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 2. Choose Your Interview Question")

        question_mode = st.radio(
            "Question source",
            [
                "✨ Generate with AI",
                "✍️ Enter manually"
            ],
            horizontal=True
        )

        question = ""

        if question_mode == "✨ Generate with AI":

            st.info(
                "Let AI generate a technical interview question "
                "based on your selected job role."
            )

            if st.button(
                "✨ Generate Interview Question",
                type="primary",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "AI is preparing your interview question..."
                    ):

                        generated = generate_interview_question(job_role)

                        st.session_state.generated_question_input = generated
                        st.session_state.generated_for_role = job_role
                        st.session_state.result = None

                except Exception as e:

                    st.error(f"Question generation failed: {e}")

            if (
                st.session_state.generated_for_role
                and st.session_state.generated_for_role != job_role
            ):
                st.warning(
                    "The selected role has changed. Generate a new question."
                )

            question = st.text_area(
                "Your Interview Question",
                key="generated_question_input",
                height=110,
                placeholder="Generate a question to get started..."
            )

        else:

            question = st.text_area(
                "Enter Your Interview Question",
                key="custom_question",
                height=110,
                placeholder="Example: Explain the difference between a list and a tuple in Python."
            )

    # --------------------------------------------------------
    # STUDENT ANSWER
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 3. Submit Your Interview Answer")

        student_answer = st.text_area(
            "Your Answer",
            height=190,
            placeholder=(
                "Write your answer here...\n\n"
                "Explain the concept clearly and include examples where possible."
            ),
            key="student_answer"
        )

        word_count = len(student_answer.split())

        st.caption(f"📝 Word count: {word_count}")

        evaluate_button = st.button(
            "🚀 Evaluate My Answer",
            type="primary",
            use_container_width=True
        )

    # --------------------------------------------------------
    # WORKFLOW EXECUTION
    # --------------------------------------------------------

    if evaluate_button:

        if not question.strip():

            st.warning("Please generate or enter an interview question.")

        elif not student_answer.strip():

            st.warning("Please enter your interview answer.")

        else:

            initial_state = {
                "job_role": job_role,
                "question": question,
                "student_answer": student_answer,
                "analysis": "",
                "score": 0,
                "feedback": "",
                "final_report": ""
            }

            try:

                with st.spinner(
                    "🤖 LangGraph is evaluating your interview answer..."
                ):

                    result = workflow_app.invoke(initial_state)

                    st.session_state.result = result
                    st.session_state.total_attempts += 1

            except Exception as e:

                st.error(f"Workflow execution failed: {e}")

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    if st.session_state.result is not None:

        result = st.session_state.result
        score = result["score"]

        st.divider()

        st.markdown(
            '<div class="section-heading">📊 Your Performance Dashboard</div>',
            unsafe_allow_html=True
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Interview Score",
                f"{score}/10"
            )

        with col2:
            st.metric(
                "Performance",
                "Good" if score >= 7 else "Needs Improvement"
            )

        with col3:
            st.metric(
                "Evaluation Status",
                "Completed"
            )

        st.progress(score / 10)

        if score >= 7:
            st.success(
                "Excellent work! Your answer meets the evaluation threshold."
            )
        else:
            st.warning(
                "Your answer needs improvement. Review the feedback below."
            )

        # Results tabs
        analysis_tab, feedback_tab, report_tab = st.tabs(
            [
                "🔍 Answer Analysis",
                "💡 Improvement Feedback",
                "📄 Final Report"
            ]
        )

        with analysis_tab:

            st.markdown("### Answer Analysis")

            st.write(result["analysis"])

            with st.expander("View Submitted Answer"):

                st.write(result["student_answer"])

        with feedback_tab:

            st.markdown("### Personalized Improvement Feedback")

            if result.get("feedback"):

                st.markdown(result["feedback"])

            else:

                st.success(
                    "No additional feedback required. "
                    "Your answer achieved the required score."
                )

        with report_tab:

            st.markdown("### Interview Evaluation Report")

            st.markdown(result["final_report"])

            st.download_button(
                label="⬇️ Download Evaluation Report",
                data=result["final_report"],
                file_name="placement_feedback_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.caption(
            "AI-generated feedback is intended for interview practice "
            "and does not represent an official hiring decision."
        )


# ============================================================
# EVALUATION HISTORY PAGE
# ============================================================

elif page == "📊 My Evaluation":

    st.markdown("## 📊 My Evaluation")

    if st.session_state.result is None:

        st.info(
            "No evaluation available yet. Complete an interview practice "
            "session to see your results here."
        )

    else:

        result = st.session_state.result

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Latest Score",
                f"{result['score']}/10"
            )

        with col2:

            st.metric(
                "Total Evaluations",
                st.session_state.total_attempts
            )

        st.markdown("### Latest Interview Details")

        st.write("**Job Role:**", result["job_role"])

        st.write("**Question:**", result["question"])

        st.write("**Score:**", f"{result['score']}/10")

        st.markdown("### Latest Feedback")

        if result.get("feedback"):
            st.write(result["feedback"])
        else:
            st.success("No additional improvement feedback required.")

        st.download_button(
            "⬇️ Download Latest Report",
            data=result["final_report"],
            file_name="placement_feedback_report.txt",
            mime="text/plain"
        )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "ℹ️ About Project":

    st.markdown("## ℹ️ About PlacementAI")

    st.write(
        "PlacementAI is an AI-powered interview practice application "
        "that evaluates student answers and generates personalized feedback."
    )

    st.markdown("### Technology Stack")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        - **Python:** Programming language
        - **LangChain:** LLM integration
        - **LangGraph:** Workflow orchestration
        - **OpenRouter:** AI model access
        """)

    with col2:

        st.markdown("""
        - **Streamlit:** User interface
        - **LangSmith:** Workflow tracing
        - **GPT-OSS:** Language model
        """)

    st.markdown("### Workflow Architecture")

    st.code("""
START
  |
  v
Analyze Answer
  |
  v
Evaluate Answer
  |
  v
Conditional Routing
  |
  +---- Score < 7 ----> Generate Feedback
  |                            |
  +---- Score >= 7 ------------+
                               |
                               v
                       Generate Report
                               |
                               v
                              END
    """, language="text")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    PlacementAI | Built with LangChain, LangGraph, Streamlit and LangSmith
    <br>
    AI-powered interview preparation for students
</div>
""", unsafe_allow_html=True)
