from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from config import Config
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

# Import services
from services.resume_parser import ResumeParser
from services.job_analyzer import JobAnalyzer
from services.gap_analyzer import GapAnalyzer
from services.ats_scanner import ATSScanner
from services.resume_optimizer import ResumeOptimizer
from services.docx_generator import DocxGenerator

# Import utilities
from utils.validators import Validators

# Import models
from models.analysis_models import CompleteAnalysisResult

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check if Claude API key is configured
        claude_configured = bool(Config.CLAUDE_API_KEY)

        return jsonify({
            'status': 'healthy',
            'claude_api': 'configured' if claude_configured else 'not_configured',
            'environment': Config.FLASK_ENV
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Main endpoint for complete 4-step resume analysis

    Accepts:
    - resume_file: File upload (PDF/DOCX/TXT) OR
    - resume_text: Plain text resume
    - job_description: Job description text (required)

    Returns:
    - JSON with complete analysis results from all 4 steps
    """
    try:
        # Get job description
        job_description = request.form.get('job_description')

        # Validate job description
        is_valid, error = Validators.validate_job_description(job_description)
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Get resume (either file or text)
        resume_text = None

        if 'resume_file' in request.files:
            # Handle file upload
            file = request.files['resume_file']

            # Validate file
            is_valid, error = Validators.validate_file(file)
            if not is_valid:
                return jsonify({'success': False, 'error': error}), 400

            # Save file temporarily
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            file.save(file_path)

            # Validate file size
            is_valid, error = Validators.validate_file_size(file_path)
            if not is_valid:
                os.remove(file_path)
                return jsonify({'success': False, 'error': error}), 400

            # Parse resume
            try:
                parsed = ResumeParser.parse_file(file_path)
                resume_text = parsed['text']
            finally:
                # Clean up temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)

        elif 'resume_text' in request.form:
            # Handle text input
            resume_text = request.form.get('resume_text')

            # Validate resume text
            is_valid, error = Validators.validate_resume_text(resume_text)
            if not is_valid:
                return jsonify({'success': False, 'error': error}), 400

        else:
            return jsonify({
                'success': False,
                'error': 'Either resume_file or resume_text is required'
            }), 400

        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())

        # Initialize services
        job_analyzer = JobAnalyzer()
        gap_analyzer = GapAnalyzer()
        ats_scanner = ATSScanner()
        resume_optimizer = ResumeOptimizer()

        # Step 1: Analyze job description
        print(f"[{analysis_id}] Step 1: Analyzing job description...")
        job_analysis = job_analyzer.analyze_job_description(job_description)

        # Step 2: Analyze resume gaps
        print(f"[{analysis_id}] Step 2: Analyzing resume gaps...")
        gap_analysis = gap_analyzer.analyze_resume_gaps(resume_text, job_analysis)

        # Step 3: Scan ATS compatibility
        print(f"[{analysis_id}] Step 3: Scanning ATS compatibility...")
        ats_scan = ats_scanner.scan_ats_compatibility(resume_text)

        # Step 4: Optimize resume
        print(f"[{analysis_id}] Step 4: Optimizing resume...")
        optimized_resume = resume_optimizer.optimize_resume(
            resume_text, job_analysis, gap_analysis, ats_scan
        )

        # Create complete analysis result
        result = CompleteAnalysisResult(
            success=True,
            analysis_id=analysis_id,
            job_analysis=job_analysis.to_dict(),
            gap_analysis=gap_analysis.to_dict(),
            ats_scan=ats_scan.to_dict(),
            optimized_resume=optimized_resume.to_dict()
        )

        print(f"[{analysis_id}] Analysis complete!")

        return jsonify(result.to_dict()), 200

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/generate-docx', methods=['POST'])
def generate_docx():
    """
    Generate and download optimized resume as DOCX file

    Accepts:
    - optimized_resume_text: The optimized resume text
    - candidate_name: Candidate name (optional, default: "Resume")

    Returns:
    - Binary DOCX file
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        optimized_text = data.get('optimized_resume_text')
        candidate_name = data.get('candidate_name', 'Resume')

        if not optimized_text:
            return jsonify({
                'success': False,
                'error': 'optimized_resume_text is required'
            }), 400

        # Generate DOCX file
        docx_file = DocxGenerator.generate_docx(optimized_text, candidate_name)

        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"optimized_resume_{timestamp}.docx"

        # Return file
        return send_file(
            docx_file,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Error generating DOCX: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'DOCX generation failed: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Validate configuration before starting
    try:
        if Config.FLASK_ENV == 'production':
            Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Note: Set CLAUDE_API_KEY in .env file for full functionality")

    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
