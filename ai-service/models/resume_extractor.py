import tika
from tika import parser
import os

# Force Tika to use its online server instead of starting a local Java-based server.
os.environ["TIKA_SERVER_ENDPOINT"] = "https://tika.apache.org/tika"

# Do not call tika.initVM() here, so it won't try to start a local Tika server.

def extract_text_from_file(file_path):
    """Extract text from a PDF or DOCX file using Apache Tika's online server."""
    parsed = parser.from_file(file_path, serverEndpoint=os.environ["TIKA_SERVER_ENDPOINT"])
    return parsed["content"].strip() if parsed["content"] else ""

# Test function (Runs locally)
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change this to your actual file path.
    text = extract_text_from_file(file_path)
    print(text[:500])  # Print first 500 characters.
