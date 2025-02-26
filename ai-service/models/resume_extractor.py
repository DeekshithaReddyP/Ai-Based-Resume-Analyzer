import os
import mimetypes

def extract_text_from_file(file_path):
    """
    Extract text from a PDF or DOCX file using alternative libraries.
    For PDFs: PyPDF2; For DOCX: python-docx.
    """
    mime, _ = mimetypes.guess_type(file_path)
    
    if mime == 'application/pdf':
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print("Error extracting PDF:", e)
            return ""
    
    elif mime in [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword'
    ]:
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print("Error extracting DOCX:", e)
            return ""
    
    else:
        print("Unsupported file type:", mime)
        return ""

# Test function (Runs locally)
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change to your actual file path
    text = extract_text_from_file(file_path)
    print(text[:500])  # Print first 500 characters
