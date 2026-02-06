import os
import re
from PyPDF2 import PdfReader
import docx2txt


class ResumeParser:
    """Service for parsing resumes from various file formats"""

    @staticmethod
    def parse_file(file_path):
        """
        Parse a resume file and extract text content

        Args:
            file_path (str): Path to the resume file

        Returns:
            dict: Parsed resume data with text content and detected sections

        Raises:
            ValueError: If file format is not supported
            Exception: If parsing fails
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        try:
            if file_ext == '.pdf':
                text = ResumeParser._parse_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                text = ResumeParser._parse_docx(file_path)
            elif file_ext == '.txt':
                text = ResumeParser._parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")

            # Detect sections
            sections = ResumeParser._detect_sections(text)

            return {
                'text': text,
                'sections': sections,
                'file_type': file_ext
            }

        except Exception as e:
            raise Exception(f"Failed to parse resume: {str(e)}")

    @staticmethod
    def parse_text(text):
        """
        Parse resume from plain text string

        Args:
            text (str): Resume text content

        Returns:
            dict: Parsed resume data with text content and detected sections
        """
        sections = ResumeParser._detect_sections(text)

        return {
            'text': text,
            'sections': sections,
            'file_type': 'text'
        }

    @staticmethod
    def _parse_pdf(file_path):
        """Extract text from PDF file"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF parsing failed: {str(e)}")

    @staticmethod
    def _parse_docx(file_path):
        """Extract text from DOCX file"""
        try:
            text = docx2txt.process(file_path)
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX parsing failed: {str(e)}")

    @staticmethod
    def _parse_txt(file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text.strip()
        except Exception as e:
            raise Exception(f"TXT parsing failed: {str(e)}")

    @staticmethod
    def _detect_sections(text):
        """
        Detect common resume sections

        Args:
            text (str): Resume text content

        Returns:
            dict: Detected sections with their positions
        """
        sections = {}

        # Common section headers (case-insensitive)
        section_patterns = {
            'contact': r'(?i)(contact\s+information|contact\s+details)',
            'summary': r'(?i)(professional\s+summary|summary|profile|objective)',
            'experience': r'(?i)(work\s+experience|professional\s+experience|experience|employment\s+history)',
            'education': r'(?i)(education|academic\s+background)',
            'skills': r'(?i)(skills|technical\s+skills|core\s+competencies|competencies)',
            'certifications': r'(?i)(certifications|certificates|licenses)',
            'projects': r'(?i)(projects|key\s+projects)',
            'awards': r'(?i)(awards|honors|achievements)',
        }

        for section_name, pattern in section_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                sections[section_name] = {
                    'found': True,
                    'position': match.start()
                }
                break  # Only take first match for each section

        return sections
