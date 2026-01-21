import streamlit as st
from pathlib import Path
import re

class FileValidator:
    """Validates uploaded files for security and content"""
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.txt', '.md', '.pdf', '.docx', '.csv'}
    
    # Maximum file size in MB
    MAX_FILE_SIZE_MB = 10
    
    @staticmethod
    def validate_file(uploaded_file):
        """
        Validates uploaded file
        Returns: (is_valid, error_message)
        """
        if uploaded_file is None:
            return False, "No file uploaded"
        
        # Check file extension
        file_extension = Path(uploaded_file.name).suffix.lower()
        if file_extension not in FileValidator.ALLOWED_EXTENSIONS:
            return False, f"File type {file_extension} not allowed. Allowed types: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}"
        
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > FileValidator.MAX_FILE_SIZE_MB:
            return False, f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({FileValidator.MAX_FILE_SIZE_MB} MB)"
        
        # Check filename for suspicious patterns
        if not FileValidator.is_safe_filename(uploaded_file.name):
            return False, "Filename contains invalid characters"
        
        return True, "File is valid"
    
    @staticmethod
    def is_safe_filename(filename):
        """Check if filename is safe (no path traversal, special chars)"""
        # Allow only alphanumeric, spaces, hyphens, underscores, and dots
        safe_pattern = re.compile(r'^[\w\s\-\.]+$')
        return safe_pattern.match(filename) is not None
    
    @staticmethod
    def read_file_content(uploaded_file):
        """
        Reads content from uploaded file
        Returns: (content, error_message)
        """
        try:
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            if file_extension in {'.txt', '.md'}:
                # Read text files
                content = uploaded_file.read().decode('utf-8')
                return content, None
            
            elif file_extension == '.csv':
                # Read CSV files
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                content = df.to_string()
                return content, None
            
            elif file_extension == '.pdf':
                # PDF reading requires PyPDF2 or pdfplumber
                try:
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    content = ""
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                    return content, None
                except ImportError:
                    return None, "PDF support requires PyPDF2. Install with: pip install PyPDF2"
            
            elif file_extension == '.docx':
                # DOCX reading requires python-docx
                try:
                    from docx import Document
                    doc = Document(uploaded_file)
                    content = "\n".join([para.text for para in doc.paragraphs])
                    return content, None
                except ImportError:
                    return None, "DOCX support requires python-docx. Install with: pip install python-docx"
            
            else:
                return None, f"Unsupported file type: {file_extension}"
                
        except UnicodeDecodeError:
            return None, "File encoding error. Please ensure the file is in UTF-8 format."
        except Exception as e:
            return None, f"Error reading file: {str(e)}"


def file_upload_section(label="Upload a file", help_text=None, key=None):
    """
    Creates a file upload section with validation
    Returns: (content, filename) or (None, None) if invalid
    """
    if help_text is None:
        help_text = f"Allowed types: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}. Max size: {FileValidator.MAX_FILE_SIZE_MB} MB"
    
    uploaded_file = st.file_uploader(
        label,
        type=[ext.replace('.', '') for ext in FileValidator.ALLOWED_EXTENSIONS],
        help=help_text,
        key=key
    )
    
    if uploaded_file is not None:
        # Validate file
        is_valid, message = FileValidator.validate_file(uploaded_file)
        
        if not is_valid:
            st.error(f"❌ {message}")
            return None, None
        
        # Read content
        content, error = FileValidator.read_file_content(uploaded_file)
        
        if error:
            st.error(f"❌ {error}")
            return None, None
        
        st.success(f"✅ File '{uploaded_file.name}' loaded successfully ({uploaded_file.size / 1024:.2f} KB)")
        return content, uploaded_file.name
    
    return None, None