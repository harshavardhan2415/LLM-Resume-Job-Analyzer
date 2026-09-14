import json
import ollama


def analyze_resume(resume_text, job_description):
    """
    Analyze a resume against a job description using Llama.
    """

    prompt = f"""
You are an expert technical recruiter.

Compare the candidate's resume with the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY a JSON object.

The JSON MUST follow this exact structure:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "resume_strengths": [],
    "resume_weaknesses": [],
    "recommendations": [],
    "interview_questions": []
}}

Rules:
- match_percentage must be a number from 0 to 100.
- matching_skills must be a list.
- missing_skills must be a list.
- resume_strengths must be a list.
- resume_weaknesses must be a list.
- recommendations must be a list.
- interview_questions must contain exactly 3 questions.
- Use double quotes for JSON strings.
- Do NOT use markdown.
- Do NOT use ```json.
- Do NOT add any text before or after the JSON.
- Make sure the JSON ends with a closing }}.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    response_text = response["message"]["content"].strip()

    print("\n--- RAW LLM RESPONSE ---")
    print(response_text)

    # Remove markdown code fences if the model adds them
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")
    response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:

        # Try to recover JSON if the model forgot the final }
        start = response_text.find("{")
        end = response_text.rfind("}")

        if start != -1 and end != -1:
            cleaned_response = response_text[start:end + 1]

            try:
                return json.loads(cleaned_response)

            except json.JSONDecodeError:
                pass

        print("\nLLM returned invalid JSON.")

        return {
            "match_percentage": 0,
            "matching_skills": [],
            "missing_skills": [],
            "resume_strengths": [],
            "resume_weaknesses": [],
            "recommendations": [],
            "interview_questions": []
        }