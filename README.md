# Resume Transformer - AI-Powered ATS Optimizer

![Resume Transformer](https://img.shields.io/badge/Status-Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Claude](https://img.shields.io/badge/Claude-Sonnet%204.5-purple)

A powerful web application that analyzes resumes against job descriptions using AI, identifies gaps, scans for ATS compatibility, and generates optimized resumes ready for download as professional .docx files.

## Features

### 4-Step Analysis Pipeline

1. **Job Description Analysis** - Extracts required skills, preferred skills, key responsibilities, and ATS keywords
2. **Resume Gap Analysis** - Compares resume against job requirements, calculates match score (0-100), identifies strengths and gaps
3. **ATS Compatibility Scan** - Analyzes resume for ATS parsing issues, provides compatibility score and recommendations
4. **Resume Optimization** - Generates ATS-optimized resume with keyword integration and professional formatting

### Key Capabilities

- Upload resumes in PDF, DOCX, or TXT format
- Paste resume text directly
- Match scoring algorithm (0-100)
- ATS compatibility scoring
- Keyword gap analysis with priority levels
- Section-by-section readability assessment
- Download optimized resume as .docx file
- Responsive web interface
- Powered by Claude Sonnet 4.5 for intelligent analysis

## Technology Stack

**Backend:**
- Python 3.11+
- Flask (Web framework)
- Anthropic Claude API (AI analysis)
- python-docx (DOCX generation)
- PyPDF2 (PDF parsing)

**Frontend:**
- HTML5, CSS3
- Vanilla JavaScript (No frameworks)
- Responsive design

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic Claude API key ([Get one here](https://console.anthropic.com/))
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yawoti/ResumePriMus.git
cd ResumePriMus
```

2. **Set up Python virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r backend/requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the `backend` directory:

```bash
cd backend
copy .env.example .env
```

Edit `.env` and add your Claude API key:

```
CLAUDE_API_KEY=your_anthropic_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

5. **Run the application**

**Option A - Using the batch script (Windows):**
```bash
cd ..
run.bat
```

**Option B - Manual start:**
```bash
cd backend
python app.py
```

6. **Open the frontend**

Open `frontend/index.html` in your web browser, or serve it via a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Usage

1. **Upload or paste your resume**
   - Click "Upload File" to select a PDF/DOCX/TXT file, or
   - Click "Paste Text" and paste your resume content

2. **Paste the job description**
   - Copy the job description from the posting and paste it into the text area

3. **Click "Analyze Resume"**
   - Wait 30-60 seconds for the AI analysis to complete

4. **Review the results**
   - **Executive Summary**: View your match score and ATS score
   - **Step 1**: See extracted job requirements and keywords
   - **Step 2**: Review your strengths and gaps
   - **Step 3**: Check ATS compatibility issues
   - **Step 4**: View your optimized resume

5. **Download your optimized resume**
   - Click "Download Optimized Resume (.docx)" to get your ATS-friendly resume

## API Endpoints

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "claude_api": "configured",
  "environment": "development"
}
```

### POST /api/analyze
Main analysis endpoint

**Request (multipart/form-data):**
- `resume_file`: File (PDF/DOCX/TXT) [optional]
- `resume_text`: String [optional]
- `job_description`: String [required]

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid",
  "results": {
    "step1_job_analysis": {...},
    "step2_gap_analysis": {...},
    "step3_ats_scan": {...},
    "step4_optimized_resume": {...}
  }
}
```

### POST /api/generate-docx
Generate DOCX file

**Request (JSON):**
```json
{
  "optimized_resume_text": "...",
  "candidate_name": "John Doe"
}
```

**Response:** Binary .docx file

## Project Structure

```
Resume Transformer/
├── backend/
│   ├── app.py                    # Flask application
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # Dependencies
│   ├── services/
│   │   ├── claude_service.py     # Claude API integration
│   │   ├── resume_parser.py      # Resume parsing
│   │   ├── job_analyzer.py       # Job analysis (Step 1)
│   │   ├── gap_analyzer.py       # Gap analysis (Step 2)
│   │   ├── ats_scanner.py        # ATS scan (Step 3)
│   │   ├── resume_optimizer.py   # Optimization (Step 4)
│   │   └── docx_generator.py     # DOCX generation
│   ├── models/
│   │   ├── prompts.py            # Claude prompts
│   │   └── analysis_models.py    # Data models
│   └── utils/
│       ├── validators.py         # Input validation
│       └── formatters.py         # Text formatting
├── frontend/
│   ├── index.html                # Main UI
│   ├── css/
│   │   ├── styles.css            # Main styles
│   │   └── analysis.css          # Analysis display
│   └── js/
│       ├── app.js                # App logic
│       ├── upload-handler.js     # File uploads
│       ├── api-client.js         # API communication
│       ├── analysis-display.js   # Results display
│       └── docx-download.js      # Download handler
├── .gitignore
├── README.md
└── run.bat                       # Windows startup script
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_API_KEY` | Anthropic API key | Required |
| `FLASK_ENV` | Environment mode | `development` |
| `FLASK_DEBUG` | Debug mode | `True` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `5242880` (5MB) |
| `ALLOWED_EXTENSIONS` | Allowed file types | `pdf,docx,txt` |
| `CORS_ORIGINS` | CORS allowed origins | `*` |

## Development

### Running Tests

```bash
cd backend
pytest tests/ -v
```

### Code Structure

- **Services**: Business logic and external API integrations
- **Models**: Data structures and prompt templates
- **Utils**: Helper functions and utilities
- **Frontend**: Static HTML/CSS/JS files

## Troubleshooting

### "Claude API key not configured"
- Make sure you've created a `.env` file in the `backend` directory
- Add your API key: `CLAUDE_API_KEY=your_key_here`
- Restart the Flask server

### "Backend API may not be running"
- Ensure the Flask server is running on port 5000
- Check for error messages in the terminal
- Try accessing http://localhost:5000/api/health directly

### File upload fails
- Check file size (max 5MB)
- Ensure file type is PDF, DOCX, or TXT
- Try pasting the text instead

### Analysis takes too long
- Normal analysis takes 30-60 seconds
- Complex resumes may take longer
- Check your internet connection
- Verify Claude API rate limits

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Claude Sonnet 4.5](https://www.anthropic.com/) by Anthropic
- Resume optimization methodology based on industry best practices
- ATS compatibility guidelines from leading recruitment platforms

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/yawoti/ResumePriMus/issues)
- Contact: [Your Email]

---

**Resume Transformer** - Transforming resumes, one analysis at a time 🚀

Built with ❤️ using Claude Code
