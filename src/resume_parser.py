from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


if __name__ == "__main__":
    pdf_path = "C:\\Users\\harsh\\OneDrive\\Desktop\\LLM_Resume_Job_Analyzer\\uploads\\Resume.pdf"
    resume_text = extract_text_from_pdf(pdf_path)

    print("\n--- RESUME TEXT ---\n")
    print(resume_text)