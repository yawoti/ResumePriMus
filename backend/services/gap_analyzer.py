import json
from services.claude_service import ClaudeService
from models.prompts import GAP_ANALYSIS_PROMPT, SYSTEM_MESSAGE
from models.analysis_models import GapAnalysisResult, JobAnalysisResult


class GapAnalyzer:
    """Service for analyzing resume gaps against job requirements (Step 2)"""

    def __init__(self):
        self.claude_service = ClaudeService()

    def analyze_resume_gaps(self, resume_text, job_analysis):
        """
        Analyze gaps between resume and job requirements

        Args:
            resume_text (str): Resume text content
            job_analysis (JobAnalysisResult or dict): Job analysis results

        Returns:
            GapAnalysisResult: Structured gap analysis data

        Raises:
            Exception: If analysis fails
        """
        try:
            # Convert job_analysis to dict if it's an object
            if isinstance(job_analysis, JobAnalysisResult):
                job_analysis_dict = job_analysis.to_dict()
            else:
                job_analysis_dict = job_analysis

            # Format job analysis as readable text
            job_analysis_text = json.dumps(job_analysis_dict, indent=2)

            # Format prompt
            prompt = GAP_ANALYSIS_PROMPT.format(
                resume_text=resume_text,
                job_analysis=job_analysis_text
            )

            # Get response from Claude as JSON
            response_data = self.claude_service.send_prompt_with_json(
                prompt=prompt,
                system_message=SYSTEM_MESSAGE
            )

            # Create result object
            result = GapAnalysisResult(
                match_score=response_data.get('match_score', 0),
                strengths=response_data.get('strengths', []),
                gaps=response_data.get('gaps', []),
                keyword_matches=response_data.get('keyword_matches', {})
            )

            return result

        except Exception as e:
            raise Exception(f"Gap analysis failed: {str(e)}")
