// API Client for Backend Communication

const API_BASE_URL = 'http://localhost:5000/api';

async function analyzeResume(resumeFile, resumeText, jobDescription) {
    /**
     * Call the /api/analyze endpoint
     *
     * @param {File|null} resumeFile - Resume file (if upload mode)
     * @param {string|null} resumeText - Resume text (if paste mode)
     * @param {string} jobDescription - Job description text
     * @returns {Promise<object>} - Analysis results
     */

    try {
        const formData = new FormData();

        // Add job description
        formData.append('job_description', jobDescription);

        // Add resume (either file or text)
        if (resumeFile) {
            formData.append('resume_file', resumeFile);
        } else if (resumeText) {
            formData.append('resume_text', resumeText);
        }

        // Make API request
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        // Parse response
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        if (!data.success) {
            throw new Error(data.error || 'Analysis returned unsuccessful');
        }

        return data.results;

    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function generateDocx(optimizedResumeText, candidateName = 'Resume') {
    /**
     * Call the /api/generate-docx endpoint
     *
     * @param {string} optimizedResumeText - Optimized resume text
     * @param {string} candidateName - Candidate name for filename
     * @returns {Promise<Blob>} - DOCX file blob
     */

    try {
        const response = await fetch(`${API_BASE_URL}/generate-docx`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                optimized_resume_text: optimizedResumeText,
                candidate_name: candidateName
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'DOCX generation failed');
        }

        // Return blob
        return await response.blob();

    } catch (error) {
        console.error('DOCX Generation Error:', error);
        throw error;
    }
}

async function checkHealth() {
    /**
     * Check API health status
     *
     * @returns {Promise<object>} - Health status
     */

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return await response.json();
    } catch (error) {
        console.error('Health check failed:', error);
        return { status: 'unreachable' };
    }
}

// Check API health on page load
document.addEventListener('DOMContentLoaded', async function() {
    const health = await checkHealth();
    console.log('API Health:', health);

    if (health.status !== 'healthy') {
        console.warn('Backend API may not be running. Please start the server.');
    }

    if (health.claude_api !== 'configured') {
        console.warn('Claude API key not configured. Please set CLAUDE_API_KEY in .env file.');
    }
});
