"""
Document Processor Module
Extracts text from .txt, .docx, and .pdf files
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


class DocumentProcessor:
    """Process various document formats and extract text content"""
    
    def __init__(self, data_dir: str):
        """
        Initialize the document processor
        
        Args:
            data_dir: Path to the data directory containing documents
        """
        self.data_dir = Path(data_dir)
        self.documents = {}  # Store doc_id -> (filename, content)
        
    def extract_txt(self, file_path: Path) -> str:
        """Extract text from .txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def extract_docx(self, file_path: Path) -> str:
        """Extract text from .docx file"""
        if DocxDocument is None:
            print("python-docx not installed. Skipping .docx files")
            return ""
        
        try:
            doc = DocxDocument(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def extract_pdf(self, file_path: Path) -> str:
        """Extract text from .pdf file"""
        if PyPDF2 is None:
            try:
                import pdfplumber
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = ''.join([page.extract_text() for page in pdf.pages])
                        return text
                except Exception as e:
                    print(f"Error reading {file_path} with pdfplumber: {e}")
                    return ""
            except ImportError:
                print("Neither PyPDF2 nor pdfplumber installed. Skipping .pdf files")
                return ""
        
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
                return text
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def load_documents(self) -> Dict[str, Tuple[str, str]]:
        """
        Load all documents from the data directory
        
        Returns:
            Dictionary: {doc_id: (filename, content)}
        """
        doc_id = 1
        
        # Process files in sorted order
        for file_path in sorted(self.data_dir.iterdir()):
            if not file_path.is_file():
                continue
            
            filename = file_path.name
            content = ""
            
            if file_path.suffix == '.txt':
                content = self.extract_txt(file_path)
            elif file_path.suffix == '.docx':
                content = self.extract_docx(file_path)
            elif file_path.suffix == '.pdf':
                content = self.extract_pdf(file_path)
            
            if content.strip():
                self.documents[doc_id] = (filename, content)
                print(f"Loaded: {filename}")
                doc_id += 1
        
        print(f"\nTotal documents loaded: {len(self.documents)}")
        return self.documents
    
    def get_document(self, doc_id: int) -> Tuple[str, str]:
        """Get document by ID"""
        return self.documents.get(doc_id, (None, None))
    
    def get_all_documents(self) -> Dict[str, Tuple[str, str]]:
        """Get all loaded documents"""
        return self.documents
