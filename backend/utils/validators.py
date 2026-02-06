import os
from werkzeug.utils import secure_filename
from config import Config


class Validators:
    """Input validation utilities"""

    @staticmethod
    def validate_file(file, allowed_extensions=None):
        """
        Validate uploaded file

        Args:
            file: FileStorage object from Flask request
            allowed_extensions: Set of allowed extensions (optional)

        Returns:
            tuple: (is_valid, error_message)
        """
        if allowed_extensions is None:
            allowed_extensions = Config.ALLOWED_EXTENSIONS

        # Check if file is present
        if not file or file.filename == '':
            return False, "No file provided"

        # Check file extension
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower().replace('.', '')

        if file_ext not in allowed_extensions:
            return False, f"File type .{file_ext} not allowed. Allowed types: {', '.join(allowed_extensions)}"

        # Check file size (we'll check this when reading the file)
        # Note: Flask doesn't easily provide file size before reading
        # We can implement this in the route handler

        return True, None

    @staticmethod
    def validate_file_size(file_path, max_size=None):
        """
        Validate file size

        Args:
            file_path: Path to the file
            max_size: Maximum allowed size in bytes (optional)

        Returns:
            tuple: (is_valid, error_message)
        """
        if max_size is None:
            max_size = Config.MAX_FILE_SIZE

        try:
            file_size = os.path.getsize(file_path)
            if file_size > max_size:
                max_mb = max_size / (1024 * 1024)
                return False, f"File too large. Maximum size: {max_mb:.1f}MB"
            return True, None
        except Exception as e:
            return False, f"Could not check file size: {str(e)}"

    @staticmethod
    def validate_text_input(text, min_length=10, max_length=50000, field_name="Input"):
        """
        Validate text input

        Args:
            text: Text string to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length
            field_name: Name of the field for error messages

        Returns:
            tuple: (is_valid, error_message)
        """
        if not text or not isinstance(text, str):
            return False, f"{field_name} is required"

        text = text.strip()

        if len(text) < min_length:
            return False, f"{field_name} must be at least {min_length} characters"

        if len(text) > max_length:
            return False, f"{field_name} must not exceed {max_length} characters"

        return True, None

    @staticmethod
    def validate_job_description(job_desc):
        """
        Validate job description input

        Args:
            job_desc: Job description text

        Returns:
            tuple: (is_valid, error_message)
        """
        return Validators.validate_text_input(
            job_desc,
            min_length=50,
            max_length=20000,
            field_name="Job description"
        )

    @staticmethod
    def validate_resume_text(resume_text):
        """
        Validate resume text input

        Args:
            resume_text: Resume text content

        Returns:
            tuple: (is_valid, error_message)
        """
        return Validators.validate_text_input(
            resume_text,
            min_length=100,
            max_length=30000,
            field_name="Resume text"
        )

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename for safe storage

        Args:
            filename: Original filename

        Returns:
            str: Sanitized filename
        """
        return secure_filename(filename)
