import streamlit as st
from pathlib import Path
import sys

# Add src folder to Python path
SRC_PATH = Path(__file__).resolve().parent / "src"
sys.path.append(str(SRC_PATH))

from resume_parser import extract_text_from_pdf
from jd_parser import clean_job_description
from llm_analyzer import analyze_resume
from skill_matcher import compare_skills


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="LLM Resume & Job Analyzer",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🤖 LLM Resume & Job Description Analyzer")

st.write(
    "Analyze how well a resume matches a job description "
    "using Llama 3.2 3B and Python."
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🧠 Model Information")

    st.write("**LLM:** Llama 3.2 3B")
    st.write("**Runtime:** Ollama")
    st.write("**Execution:** Local")

    st.divider()

    st.info(
        "Your resume is processed locally using "
        "the Llama model running through Ollama."
    )


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

st.subheader("1️⃣ Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload a PDF resume",
    type=["pdf"]
)


# --------------------------------------------------
# Job Description
# --------------------------------------------------

st.subheader("2️⃣ Enter Job Description")

job_description = st.text_area(
    "Paste the job description below:",
    height=300,
    placeholder="Paste the complete job description here..."
)


st.divider()


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
):

    if uploaded_file is None:

        st.error("Please upload a resume PDF.")

        st.stop()

    if not job_description.strip():

        st.error("Please enter a job description.")

        st.stop()


    # --------------------------------------------------
    # Save uploaded file temporarily
    # --------------------------------------------------

    uploads_folder = Path("uploads")
    uploads_folder.mkdir(exist_ok=True)

    resume_path = uploads_folder / uploaded_file.name

    with open(resume_path, "wb") as file:

        file.write(uploaded_file.getbuffer())


    # --------------------------------------------------
    # Extract Resume Text
    # --------------------------------------------------

    with st.spinner("📄 Reading resume..."):

        resume_text = extract_text_from_pdf(
            resume_path
        )


    if not resume_text:

        st.error(
            "Could not extract text from this PDF. "
            "It may be an image/scanned PDF."
        )

        st.stop()


    # --------------------------------------------------
    # Clean Job Description
    # --------------------------------------------------

    job_description = clean_job_description(
        job_description
    )


    # --------------------------------------------------
    # Rule-Based Skill Matching
    # --------------------------------------------------

    with st.spinner("🔍 Comparing skills..."):

        skill_results = compare_skills(
            resume_text,
            job_description
        )


    # --------------------------------------------------
    # LLM Analysis
    # --------------------------------------------------

    with st.spinner(
        "🧠 Llama is analyzing your resume..."
    ):

        llm_results = analyze_resume(
            resume_text,
            job_description
        )


    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    st.success("Analysis completed!")

    st.divider()

    st.subheader("📊 Analysis Results")


    # --------------------------------------------------
    # Scores
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Rule-Based Skill Match",
            f"{skill_results['match_percentage']}%"
        )


    with col2:

        st.metric(
            "LLM Match Score",
            f"{llm_results['match_percentage']}%"
        )


    st.divider()


    # --------------------------------------------------
    # Matching Skills
    # --------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Matching Skills")

        matching_skills = llm_results[
            "matching_skills"
        ]

        if matching_skills:

            for skill in matching_skills:

                st.write(f"• {skill}")

        else:

            st.write("No matching skills identified.")


    # --------------------------------------------------
    # Missing Skills
    # --------------------------------------------------

    with col2:

        st.subheader("❌ Missing Skills")

        missing_skills = llm_results[
            "missing_skills"
        ]

        if missing_skills:

            for skill in missing_skills:

                st.write(f"• {skill}")

        else:

            st.write("No major missing skills identified.")


    st.divider()


    # --------------------------------------------------
    # Strengths & Weaknesses
    # --------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("💪 Resume Strengths")

        for item in llm_results["resume_strengths"]:

            st.write(f"• {item}")


    with col2:

        st.subheader("⚠️ Areas to Improve")

        for item in llm_results["resume_weaknesses"]:

            st.write(f"• {item}")


    st.divider()


    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    st.subheader("💡 Recommendations")

    for recommendation in llm_results[
        "recommendations"
    ]:

        st.write(f"• {recommendation}")


    st.divider()


    # --------------------------------------------------
    # Interview Questions
    # --------------------------------------------------

    st.subheader("🎯 Interview Questions")

    for index, question in enumerate(
        llm_results["interview_questions"],
        start=1
    ):

        st.write(
            f"**{index}.** {question}"
        )


    st.divider()


    # --------------------------------------------------
    # Detected Skills
    # --------------------------------------------------

    with st.expander("🔎 View Detected Skills"):

        st.write(
            "**Skills detected in resume:**"
        )

        st.write(
            ", ".join(
                skill_results["resume_skills"]
            )
        )

        st.write(
            "**Skills detected in job description:**"
        )

        st.write(
            ", ".join(
                skill_results["job_skills"]
            )
        )