// DOCX Download Handler

document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('download-btn');

    downloadBtn.addEventListener('click', async function() {
        if (!currentAnalysisResults) {
            alert('No analysis results available. Please analyze a resume first.');
            return;
        }

        const optimizedText = currentAnalysisResults.step4_optimized_resume?.formatted_text;

        if (!optimizedText) {
            alert('No optimized resume available.');
            return;
        }

        // Disable button and show loading
        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Generating DOCX...';

        try {
            // Call API to generate DOCX
            const blob = await generateDocx(optimizedText);

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;

            // Generate filename with timestamp
            const timestamp = new Date().toISOString().slice(0,10);
            a.download = `optimized_resume_${timestamp}.docx`;

            // Trigger download
            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Success message
            showSuccessMessage('Resume downloaded successfully!');

        } catch (error) {
            console.error('Download error:', error);
            alert('Failed to download resume: ' + error.message);
        } finally {
            // Re-enable button
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Download Optimized Resume (.docx)';
        }
    });
});

function showSuccessMessage(message) {
    // Create success message element
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    successDiv.textContent = message;

    document.body.appendChild(successDiv);

    // Remove after 3 seconds
    setTimeout(() => {
        successDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(successDiv);
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
