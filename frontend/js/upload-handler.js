// File Upload Handler

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('resume-file');
    const fileNameDisplay = document.getElementById('file-name');

    fileInput.addEventListener('change', function(e) {
        if (this.files && this.files.length > 0) {
            const file = this.files[0];
            const fileName = file.name;
            const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB

            // Display file name and size
            fileNameDisplay.textContent = `${fileName} (${fileSize} MB)`;
            fileNameDisplay.classList.add('visible');

            // Validate file size
            const maxSize = 5; // 5MB
            if (parseFloat(fileSize) > maxSize) {
                alert(`File is too large. Maximum size is ${maxSize}MB`);
                this.value = ''; // Clear the input
                fileNameDisplay.classList.remove('visible');
                return;
            }

            // Validate file type
            const allowedTypes = ['.pdf', '.docx', '.txt'];
            const fileExt = '.' + fileName.split('.').pop().toLowerCase();

            if (!allowedTypes.includes(fileExt)) {
                alert(`Invalid file type. Allowed types: PDF, DOCX, TXT`);
                this.value = ''; // Clear the input
                fileNameDisplay.classList.remove('visible');
                return;
            }

        } else {
            fileNameDisplay.classList.remove('visible');
        }
    });
});
