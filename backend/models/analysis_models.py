from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import json


@dataclass
class JobAnalysisResult:
    """Result from job description analysis (Step 1)"""
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    key_responsibilities: List[str] = field(default_factory=list)
    ats_keywords: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class GapItem:
    """Individual gap item"""
    keyword: str
    priority: str
    suggestion: str


@dataclass
class GapAnalysisResult:
    """Result from resume gap analysis (Step 2)"""
    match_score: int = 0
    strengths: List[str] = field(default_factory=list)
    gaps: List[Dict[str, str]] = field(default_factory=list)
    keyword_matches: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ATSScanResult:
    """Result from ATS compatibility scan (Step 3)"""
    ats_score: int = 0
    issues: Dict[str, List[str]] = field(default_factory=lambda: {
        "formatting": [],
        "content": [],
        "keywords": []
    })
    section_readability: Dict[str, str] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class OptimizedResumeResult:
    """Result from resume optimization (Step 4)"""
    formatted_text: str = ""
    original_length: int = 0
    optimized_length: int = 0

    def to_dict(self):
        return {
            "formatted_text": self.formatted_text,
            "original_length": self.original_length,
            "optimized_length": self.optimized_length
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class CompleteAnalysisResult:
    """Complete analysis result containing all 4 steps"""
    success: bool = True
    analysis_id: str = ""
    job_analysis: Dict[str, Any] = field(default_factory=dict)
    gap_analysis: Dict[str, Any] = field(default_factory=dict)
    ats_scan: Dict[str, Any] = field(default_factory=dict)
    optimized_resume: Dict[str, Any] = field(default_factory=dict)
    error: str = None

    def to_dict(self):
        result = {
            "success": self.success,
            "analysis_id": self.analysis_id,
            "results": {
                "step1_job_analysis": self.job_analysis,
                "step2_gap_analysis": self.gap_analysis,
                "step3_ats_scan": self.ats_scan,
                "step4_optimized_resume": self.optimized_resume
            }
        }
        if self.error:
            result["error"] = self.error
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)
