import os

def validate_file_extension(file_path):
    """Ensure file format is supported (PDF, DOCX)."""
    valid_extensions = [".pdf", ".docx"]
    return os.path.splitext(file_path)[1] in valid_extensions
 
