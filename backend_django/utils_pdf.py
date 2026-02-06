import PyPDF2
from io import BytesIO

async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file content"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
