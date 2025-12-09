/**
 * ModelYourData - Upload Page JavaScript
 * Handles drag & drop file upload functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('csv-file-input');
    const filePreview = document.getElementById('file-preview');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const removeBtn = document.getElementById('remove-file');
    const uploadBtn = document.getElementById('upload-btn');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    
    let selectedFile = null;
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Highlight dropzone when dragging over
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropzone.classList.add('dragover');
    }
    
    function unhighlight() {
        dropzone.classList.remove('dragover');
    }
    
    // Handle dropped files
    dropzone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
    
    // Handle file selection via input
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });
    
    // Click on dropzone to select file
    dropzone.addEventListener('click', function(e) {
        if (e.target.tagName !== 'LABEL' && e.target.tagName !== 'INPUT') {
            fileInput.click();
        }
    });
    
    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            // Validate file
            if (!validateFile(file)) return;
            
            selectedFile = file;
            showFilePreview(file);
        }
    }
    
    function validateFile(file) {
        hideError();
        
        // Check file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showError('Only CSV files are allowed.');
            return false;
        }
        
        // Check file size (10MB limit)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            showError('File size must be under 10MB.');
            return false;
        }
        
        // Check if file is empty
        if (file.size === 0) {
            showError('The uploaded file is empty.');
            return false;
        }
        
        return true;
    }
    
    function showFilePreview(file) {
        fileName.textContent = file.name;
        fileSize.textContent = Utils.formatFileSize(file.size);
        filePreview.style.display = 'block';
        dropzone.style.display = 'none';
    }
    
    function hideFilePreview() {
        filePreview.style.display = 'none';
        dropzone.style.display = 'block';
        selectedFile = null;
        fileInput.value = '';
    }
    
    function showError(message) {
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
    }
    
    function hideError() {
        errorMessage.style.display = 'none';
    }
    
    function showProgress() {
        progressContainer.style.display = 'block';
        filePreview.style.display = 'none';
    }
    
    function updateProgress(percent, text) {
        progressFill.style.width = percent + '%';
        progressText.textContent = text;
    }
    
    function hideProgress() {
        progressContainer.style.display = 'none';
    }
    
    // Remove file button
    removeBtn.addEventListener('click', function() {
        hideFilePreview();
        hideError();
    });
    
    // Upload button
    uploadBtn.addEventListener('click', async function() {
        if (!selectedFile) return;
        
        hideError();
        showProgress();
        updateProgress(0, 'Preparing upload...');
        
        const formData = new FormData();
        formData.append('csv_file', selectedFile);
        
        try {
            // Create XMLHttpRequest for progress tracking
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    updateProgress(percent, `Uploading... ${percent}%`);
                }
            });
            
            xhr.addEventListener('load', function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        updateProgress(100, 'Upload complete! Redirecting...');
                        setTimeout(() => {
                            window.location.href = response.redirect_url;
                        }, 500);
                    } else {
                        hideProgress();
                        hideFilePreview();
                        showError(response.errors?.csv_file?.[0] || 'Upload failed');
                        dropzone.style.display = 'block';
                    }
                } else {
                    const response = JSON.parse(xhr.responseText);
                    hideProgress();
                    hideFilePreview();
                    showError(response.errors?.csv_file?.[0] || 'Upload failed');
                    dropzone.style.display = 'block';
                }
            });
            
            xhr.addEventListener('error', function() {
                hideProgress();
                hideFilePreview();
                showError('Network error. Please try again.');
                dropzone.style.display = 'block';
            });
            
            xhr.open('POST', '/upload/');
            xhr.setRequestHeader('X-CSRFToken', Utils.getCSRFToken());
            xhr.send(formData);
            
        } catch (error) {
            hideProgress();
            hideFilePreview();
            showError(error.message || 'An error occurred during upload.');
            dropzone.style.display = 'block';
        }
    });
});
