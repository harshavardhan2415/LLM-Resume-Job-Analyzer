import re


COMMON_SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "statistics",
    "data analysis",
    "data visualization",
    "etl",
    "aws",
    "azure",
    "gcp",
    "spark",
    "databricks",
    "snowflake",
    "git",
    "docker",
    "llm",
    "rag",
    "nlp",
    "tensorflow",
    "pytorch"
]


def extract_skills(text):
    """
    Extract known technical skills from text.
    """

    text = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)


def compare_skills(resume_text, job_description):
    """
    Compare skills between resume and job description.
    """

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matching_skills = sorted(resume_skills.intersection(job_skills))

    missing_skills = sorted(job_skills - resume_skills)

    if job_skills:
        match_percentage = round(
            len(matching_skills) / len(job_skills) * 100,
            2
        )
    else:
        match_percentage = 0

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }