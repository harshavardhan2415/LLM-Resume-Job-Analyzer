def clean_job_description(job_description):
    """
    Clean and prepare a job description for analysis.
    """

    if not job_description:
        return ""

    # Remove unnecessary whitespace
    job_description = " ".join(job_description.split())

    return job_description.strip()


def load_job_description(file_path):
    """
    Load a job description from a text file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        job_description = file.read()

    return clean_job_description(job_description)


if __name__ == "__main__":
    print("Job description parser is ready!")