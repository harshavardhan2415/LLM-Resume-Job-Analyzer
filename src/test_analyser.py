from pathlib import Path

from resume_parser import extract_text_from_pdf
from jd_parser import load_job_description
from llm_analyzer import analyze_resume
from skill_matcher import compare_skills


project_folder = Path(__file__).resolve().parent.parent


# -----------------------------
# File paths
# -----------------------------

resume_path = project_folder / "uploads" / "Resume.pdf"

jd_path = (
    project_folder
    / "data"
    / "sample_job_descriptions"
    / "data_analyst.txt"
)


# -----------------------------
# Extract resume
# -----------------------------

print("Reading resume...")

resume_text = extract_text_from_pdf(resume_path)


# -----------------------------
# Read job description
# -----------------------------

print("Reading job description...")

job_description = load_job_description(jd_path)


# -----------------------------
# Skill matching
# -----------------------------

print("Running skill matching...")

skill_results = compare_skills(
    resume_text,
    job_description
)


print("\n==============================")
print("RULE-BASED SKILL MATCH")
print("==============================")

print(
    "Match:",
    skill_results["match_percentage"],
    "%"
)

print(
    "Matching skills:",
    skill_results["matching_skills"]
)

print(
    "Missing skills:",
    skill_results["missing_skills"]
)


# -----------------------------
# LLM analysis
# -----------------------------

print("\nSending resume to Llama...")

llm_results = analyze_resume(
    resume_text,
    job_description
)


print("\n==============================")
print("LLM ANALYSIS")
print("==============================")

for key, value in llm_results.items():

    print(f"\n{key.upper()}:")

    if isinstance(value, list):

        for item in value:
            print("-", item)

    else:

        print(value)