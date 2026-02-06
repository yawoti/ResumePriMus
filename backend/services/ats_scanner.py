from services.claude_service import ClaudeService
from models.prompts import ATS_SCAN_PROMPT, SYSTEM_MESSAGE
from models.analysis_models import ATSScanResult


class ATSScanner:
    """Service for scanning resume ATS compatibility (Step 3)"""

    def __init__(self):
        self.claude_service = ClaudeService()

    def scan_ats_compatibility(self, resume_text):
        """
        Scan resume for ATS compatibility issues

        Args:
            resume_text (str): Resume text content

        Returns:
            ATSScanResult: Structured ATS scan data

        Raises:
            Exception: If scanning fails
        """
        try:
            # Format prompt
            prompt = ATS_SCAN_PROMPT.format(resume_text=resume_text)

            # Get response from Claude as JSON
            response_data = self.claude_service.send_prompt_with_json(
                prompt=prompt,
                system_message=SYSTEM_MESSAGE
            )

            # Create result object
            result = ATSScanResult(
                ats_score=response_data.get('ats_score', 0),
                issues=response_data.get('issues', {
                    "formatting": [],
                    "content": [],
                    "keywords": []
                }),
                section_readability=response_data.get('section_readability', {}),
                recommendations=response_data.get('recommendations', [])
            )

            return result

        except Exception as e:
            raise Exception(f"ATS scanning failed: {str(e)}")
