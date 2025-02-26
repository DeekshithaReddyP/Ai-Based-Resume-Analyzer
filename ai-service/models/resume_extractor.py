import tika
from tika import parser
import os
import json

# Force Tika to use its online server instead of starting a local Java-based server.
os.environ["TIKA_SERVER_ENDPOINT"] = "https://tika.apache.org/tika"

# Do not call tika.initVM() since it attempts to start a local Java VM.
# Instead, we rely on the online endpoint.

def extract_text_from_file(file_path):
    """Extract text from a PDF or DOCX file using Apache Tika's online server."""
    try:
        # Attempt to parse the file using Tika's online server.
        parsed = parser.from_file(file_path, serverEndpoint=os.environ["TIKA_SERVER_ENDPOINT"])
        # Get content and return it (if available)
        content = parsed.get("content", "")
        return content.strip() if content else ""
    except json.decoder.JSONDecodeError as e:
        # Log JSON decode errors (empty or invalid response)
        print("JSONDecodeError during Tika parsing:", e)
        return ""
    except Exception as e:
        # Log any other errors that occur during parsing.
        print("Error during Tika parsing:", e)
        return ""

# Test function (Runs locally)
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change this to your actual file path.
    text = extract_text_from_file(file_path)
    print(text[:500])  # Print first 500 characters.
