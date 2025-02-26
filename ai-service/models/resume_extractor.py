import tika
from tika import parser
import os
import json

# Force Tika to use its online server
os.environ["TIKA_SERVER_ENDPOINT"] = "https://tika.apache.org/tika"

# We don't call tika.initVM() since we don't want a local Java VM.

def extract_text_from_file(file_path):
    """Extract text from a PDF or DOCX file using Apache Tika's online server via a POST request."""
    try:
        # Read the file as bytes
        with open(file_path, "rb") as f:
            file_data = f.read()
        # Use from_buffer to send file data via POST (which the remote server accepts)
        parsed = parser.from_buffer(file_data, serverEndpoint=os.environ["TIKA_SERVER_ENDPOINT"])
        content = parsed.get("content", "")
        return content.strip() if content else ""
    except json.decoder.JSONDecodeError as e:
        print("JSONDecodeError during Tika parsing:", e)
        return ""
    except Exception as e:
        print("Error during Tika parsing:", e)
        return ""

# Test function (Runs locally)
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change to your actual file path
    text = extract_text_from_file(file_path)
    print(text[:500])  # Print first 500 characters
