// Main Application Logic

document.addEventListener('DOMContentLoaded', function() {
    console.log('Resume Transformer initialized');

    // Initialize upload handler
    initializeUploadToggle();

    // Initialize analyze button
    initializeAnalyzeButton();

    // Initialize tabs
    initializeTabs();
});

function initializeUploadToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const fileMode = document.getElementById('file-mode');
    const textMode = document.getElementById('text-mode');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            toggleButtons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            // Show/hide appropriate input mode
            const mode = this.dataset.mode;
            if (mode === 'file') {
                fileMode.style.display = 'block';
                textMode.style.display = 'none';
            } else {
                fileMode.style.display = 'none';
                textMode.style.display = 'block';
            }
        });
    });
}

function initializeAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyze-btn');
    analyzeBtn.addEventListener('click', handleAnalyze);
}

async function handleAnalyze() {
    // Hide previous results and errors
    hideElement('results-section');
    hideElement('error-message');

    // Get input values
    const jobDescription = document.getElementById('job-description').value.trim();

    // Validate job description
    if (!jobDescription) {
        showError('Please provide a job description');
        return;
    }

    // Get resume (either file or text)
    const activeMode = document.querySelector('.toggle-btn.active').dataset.mode;
    let resumeFile = null;
    let resumeText = null;

    if (activeMode === 'file') {
        const fileInput = document.getElementById('resume-file');
        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Please upload a resume file');
            return;
        }
        resumeFile = fileInput.files[0];
    } else {
        resumeText = document.getElementById('resume-text').value.trim();
        if (!resumeText) {
            showError('Please paste your resume text');
            return;
        }
    }

    // Show loading
    showElement('loading');
    disableAnalyzeButton(true);

    try {
        // Call API
        const results = await analyzeResume(resumeFile, resumeText, jobDescription);

        // Hide loading
        hideElement('loading');

        // Display results
        displayAnalysisResults(results);

        // Show results section
        showElement('results-section');

        // Scroll to results
        document.getElementById('results-section').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (error) {
        hideElement('loading');
        showError(error.message || 'Analysis failed. Please try again.');
        console.error('Analysis error:', error);
    } finally {
        disableAnalyzeButton(false);
    }
}

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;

            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

function showElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }
}

function hideElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

function showError(message) {
    const errorElement = document.getElementById('error-message');
    errorElement.textContent = message;
    errorElement.style.display = 'block';

    // Scroll to error
    errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function disableAnalyzeButton(disabled) {
    const analyzeBtn = document.getElementById('analyze-btn');
    analyzeBtn.disabled = disabled;
    if (disabled) {
        analyzeBtn.style.opacity = '0.6';
        analyzeBtn.style.cursor = 'not-allowed';
    } else {
        analyzeBtn.style.opacity = '1';
        analyzeBtn.style.cursor = 'pointer';
    }
}
