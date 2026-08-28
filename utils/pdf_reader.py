from pypdf import PdfReader

def extract_text(uploaded_file):
    """Extract text from a PDF or plain text upload."""
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return uploaded_file.getvalue().decode("utf-8", errors="ignore")
