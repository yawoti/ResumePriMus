import json
from services.claude_service import ClaudeService
from models.prompts import RESUME_OPTIMIZATION_PROMPT, SYSTEM_MESSAGE
from models.analysis_models import (
    OptimizedResumeResult,
    JobAnalysisResult,
    GapAnalysisResult,
    ATSScanResult
)


class ResumeOptimizer:
    """Service for optimizing resumes (Step 4)"""

    def __init__(self):
        self.claude_service = ClaudeService()

    def optimize_resume(self, resume_text, job_analysis, gap_analysis, ats_scan):
        """
        Generate optimized resume based on all analysis results

        Args:
            resume_text (str): Original resume text
            job_analysis: Job analysis results (JobAnalysisResult or dict)
            gap_analysis: Gap analysis results (GapAnalysisResult or dict)
            ats_scan: ATS scan results (ATSScanResult or dict)

        Returns:
            OptimizedResumeResult: Optimized resume data

        Raises:
            Exception: If optimization fails
        """
        try:
            # Convert analysis objects to dicts if needed
            if isinstance(job_analysis, JobAnalysisResult):
                job_analysis_dict = job_analysis.to_dict()
            else:
                job_analysis_dict = job_analysis

            if isinstance(gap_analysis, GapAnalysisResult):
                gap_analysis_dict = gap_analysis.to_dict()
            else:
                gap_analysis_dict = gap_analysis

            if isinstance(ats_scan, ATSScanResult):
                ats_scan_dict = ats_scan.to_dict()
            else:
                ats_scan_dict = ats_scan

            # Format analysis results as readable text
            job_analysis_text = json.dumps(job_analysis_dict, indent=2)
            gap_analysis_text = json.dumps(gap_analysis_dict, indent=2)
            ats_scan_text = json.dumps(ats_scan_dict, indent=2)

            # Format prompt
            prompt = RESUME_OPTIMIZATION_PROMPT.format(
                resume_text=resume_text,
                job_analysis=job_analysis_text,
                gap_analysis=gap_analysis_text,
                ats_scan=ats_scan_text
            )

            # Get response from Claude (plain text, not JSON)
            optimized_text = self.claude_service.send_prompt(
                prompt=prompt,
                system_message=SYSTEM_MESSAGE,
                max_tokens=8192,  # Larger for complete resume
                temperature=0.5   # Balanced creativity and consistency
            )

            # Create result object
            result = OptimizedResumeResult(
                formatted_text=optimized_text.strip(),
                original_length=len(resume_text),
                optimized_length=len(optimized_text)
            )

            return result

        except Exception as e:
            raise Exception(f"Resume optimization failed: {str(e)}")
