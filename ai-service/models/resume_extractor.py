import tika
from tika import parser

# Initialize Apache Tika
tika.initVM()

def extract_text_from_file(file_path):
    """Extract text from a PDF or DOCX file using Apache Tika."""
    parsed = parser.from_file(file_path)
    return parsed["content"].strip() if parsed["content"] else ""

# Test function
if __name__ == "__main__":
    file_path = "../sample_resume.pdf"  # Change this to an actual file path
    text = extract_text_from_file(file_path)
    print(text[:500])  # Print first 500 characters
