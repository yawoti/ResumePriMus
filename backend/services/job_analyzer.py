from services.claude_service import ClaudeService
from models.prompts import JOB_ANALYSIS_PROMPT, SYSTEM_MESSAGE
from models.analysis_models import JobAnalysisResult


class JobAnalyzer:
    """Service for analyzing job descriptions (Step 1)"""

    def __init__(self):
        self.claude_service = ClaudeService()

    def analyze_job_description(self, job_description):
        """
        Analyze job description and extract key information

        Args:
            job_description (str): Job description text

        Returns:
            JobAnalysisResult: Structured job analysis data

        Raises:
            Exception: If analysis fails
        """
        try:
            # Format prompt with job description
            prompt = JOB_ANALYSIS_PROMPT.format(job_description=job_description)

            # Get response from Claude as JSON
            response_data = self.claude_service.send_prompt_with_json(
                prompt=prompt,
                system_message=SYSTEM_MESSAGE
            )

            # Create result object
            result = JobAnalysisResult(
                required_skills=response_data.get('required_skills', []),
                preferred_skills=response_data.get('preferred_skills', []),
                key_responsibilities=response_data.get('key_responsibilities', []),
                ats_keywords=response_data.get('ats_keywords', [])
            )

            return result

        except Exception as e:
            raise Exception(f"Job description analysis failed: {str(e)}")
