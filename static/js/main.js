// Show file preview when a file is selected
function showFilePreview(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
}

// Toggle visibility of file preview elements
document.addEventListener('DOMContentLoaded', function() {
    // For spiral file input
    const spiralInput = document.getElementById('spiral');
    if (spiralInput) {
        spiralInput.addEventListener('change', function() {
            showFilePreview(this, 'spiralPreview');
        });
    }
    
    // For MRI file input
    const mriInput = document.getElementById('mri');
    if (mriInput) {
        mriInput.addEventListener('change', function() {
            showFilePreview(this, 'mriPreview');
        });
    }
    
    // Form validation
    const form = document.getElementById('assessmentForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    }
});

// Custom form validation
function validateForm() {
    const spiralInput = document.getElementById('spiral');
    
    // Check if spiral file is provided (required)
    if (!spiralInput || !spiralInput.files || spiralInput.files.length === 0) {
        alert('Please upload a spiral drawing image');
        return false;
    }
    
    // Check at least one symptom is answered
    const symptomInputs = document.querySelectorAll('input[type="radio"]:checked');
    if (symptomInputs.length < 7) {  // We have 7 symptom questions
        alert('Please answer all symptom questions');
        return false;
    }
    
    return true;
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
