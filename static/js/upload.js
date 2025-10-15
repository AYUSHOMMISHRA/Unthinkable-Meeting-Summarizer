/* ============================================
   MEETING SUMMARIZER - UPLOAD HANDLER
   Comprehensive File Upload with Drag & Drop
   ============================================ */

// ============================================
// 1. DOM ELEMENTS SELECTION
// ============================================
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const progressBar = document.getElementById('progressBar');
const progressBarFill = document.querySelector('.progress-bar');
const progressText = document.getElementById('progressText');
const processButton = document.getElementById('processButton');
const removeFileButton = document.getElementById('removeFile');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const fileDuration = document.getElementById('fileDuration');

// Global variable to store selected file
let selectedFile = null;

// ============================================
// 2. DRAG-AND-DROP EVENT LISTENERS
// ============================================

/**
 * Prevent default behavior for dragover event
 * Add visual feedback with 'dragover' class
 */
uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.stopPropagation();
  uploadZone.classList.add('dragover');
});

/**
 * Remove dragover class when drag leaves the zone
 */
uploadZone.addEventListener('dragleave', (e) => {
  e.preventDefault();
  e.stopPropagation();
  uploadZone.classList.remove('dragover');
});

/**
 * Handle file drop event
 * Prevent default behavior, get files, and process the first file
 */
uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  e.stopPropagation();
  uploadZone.classList.remove('dragover');
  
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

/**
 * Make the entire upload zone clickable
 */
uploadZone.addEventListener('click', () => {
  fileInput.click();
});

// ============================================
// 3. FILE INPUT CHANGE LISTENER
// ============================================

/**
 * Trigger when user clicks and selects file through file dialog
 * Process the selected file
 */
fileInput.addEventListener('change', (e) => {
  const files = e.target.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

// ============================================
// 4. HANDLE FILE FUNCTION
// ============================================

/**
 * Main function to handle file selection
 * Validates file, displays info, and enables processing
 * 
 * @param {File} file - The selected audio file
 */
async function handleFile(file) {
  // Validate file type and size
  if (!validateFile(file)) {
    return;
  }
  
  // Store the selected file
  selectedFile = file;
  
  // Display file name
  fileName.textContent = file.name;
  
  // Display file size
  fileSize.textContent = formatFileSize(file.size);
  
  // Get and display audio duration
  try {
    const duration = await getAudioDuration(file);
    fileDuration.textContent = duration;
  } catch (error) {
    console.error('Error getting audio duration:', error);
    fileDuration.textContent = 'Unknown';
  }
  
  // Show file preview card with animation
  filePreview.classList.remove('d-none');
  filePreview.classList.add('slide-up');
  
  // Enable process button
  processButton.disabled = false;
  
  // Hide upload zone (optional - makes UI cleaner)
  uploadZone.style.opacity = '0.5';
}

// ============================================
// 5. VALIDATE FILE FUNCTION
// ============================================

/**
 * Validate file type and size
 * Shows alert if validation fails
 * 
 * @param {File} file - The file to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateFile(file) {
  // Allowed audio file types
  const allowedTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav', 'audio/x-m4a', 'audio/m4a'];
  const allowedExtensions = ['.mp3', '.wav', '.m4a'];
  
  // Check file type
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  const isValidType = allowedTypes.includes(file.type) || allowedExtensions.includes(fileExtension);
  
  if (!isValidType) {
    alert('❌ Invalid file type! Please upload an MP3, WAV, or M4A audio file.');
    return false;
  }
  
  // Check file size (max 100MB)
  const maxSize = 100 * 1024 * 1024; // 100MB in bytes
  if (file.size > maxSize) {
    alert('❌ File too large! Maximum file size is 100MB.\n\nYour file: ' + formatFileSize(file.size));
    return false;
  }
  
  // File is valid
  return true;
}

// ============================================
// 6. FORMAT FILE SIZE FUNCTION
// ============================================

/**
 * Convert bytes to human-readable file size
 * 
 * @param {number} bytes - File size in bytes
 * @returns {string} - Formatted string like "2.5 MB" or "850 KB"
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  // Format to 2 decimal places for MB, 1 for KB
  const decimals = i >= 2 ? 2 : 1;
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
}

// ============================================
// 7. GET AUDIO DURATION FUNCTION
// ============================================

/**
 * Get audio file duration using HTML5 Audio API
 * Returns duration in MM:SS format
 * 
 * @param {File} file - Audio file
 * @returns {Promise<string>} - Duration in MM:SS format
 */
function getAudioDuration(file) {
  return new Promise((resolve, reject) => {
    // Create FileReader to read file as Data URL
    const reader = new FileReader();
    
    reader.onload = function(e) {
      // Create Audio element
      const audio = new Audio();
      
      audio.onloadedmetadata = function() {
        // Get duration in seconds
        const durationSeconds = Math.floor(audio.duration);
        
        // Convert to MM:SS format
        const minutes = Math.floor(durationSeconds / 60);
        const seconds = durationSeconds % 60;
        
        // Format with leading zeros
        const formattedDuration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        resolve(formattedDuration);
      };
      
      audio.onerror = function() {
        reject(new Error('Could not load audio file'));
      };
      
      // Set audio source to the file data URL
      audio.src = e.target.result;
    };
    
    reader.onerror = function() {
      reject(new Error('Could not read file'));
    };
    
    // Read file as Data URL
    reader.readAsDataURL(file);
  });
}

// ============================================
// 8. SIMULATE UPLOAD FUNCTION
// ============================================

/**
 * Simulate file upload with progress bar animation
 * Called when user clicks "Process Meeting" button
 * Stores file info and redirects to processing page
 */
function simulateUpload() {
  if (!selectedFile) {
    alert('⚠️ Please select a file first!');
    return;
  }
  
  // Disable process button to prevent double submission
  processButton.disabled = true;
  processButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Processing...';
  
  // Show progress bar with animation
  progressBar.classList.remove('d-none');
  progressBar.classList.add('slide-up');
  
  let progress = 0;
  const interval = 30; // Update every 30ms
  const totalDuration = 3000; // 3 seconds total
  const increment = 100 / (totalDuration / interval);
  
  // Animate progress bar from 0 to 100%
  const uploadInterval = setInterval(() => {
    progress += increment;
    
    if (progress >= 100) {
      progress = 100;
      clearInterval(uploadInterval);
      
      // Store file information in localStorage for processing page
      const fileInfo = {
        name: selectedFile.name,
        size: formatFileSize(selectedFile.size),
        duration: fileDuration.textContent,
        timestamp: new Date().toISOString(),
        uploadedAt: new Date().toLocaleString()
      };
      
      localStorage.setItem('currentMeeting', JSON.stringify(fileInfo));
      
      // Update progress text
      progressText.textContent = 'Upload complete! Redirecting...';
      
      // Redirect to processing page after a short delay
      setTimeout(() => {
        window.location.href = '/processing';
      }, 500);
    } else {
      // Update progress bar and text
      progressBarFill.style.width = progress + '%';
      progressText.textContent = `Uploading... ${Math.floor(progress)}%`;
    }
  }, interval);
}

// ============================================
// 9. REMOVE FILE FUNCTION
// ============================================

/**
 * Clear selected file and reset UI to initial state
 * Called when user clicks remove/cancel button
 */
function removeFile() {
  // Clear selected file
  selectedFile = null;
  
  // Reset file input
  fileInput.value = '';
  
  // Hide file preview with animation
  filePreview.classList.add('d-none');
  filePreview.classList.remove('slide-up');
  
  // Hide and reset progress bar
  progressBar.classList.add('d-none');
  progressBarFill.style.width = '0%';
  progressText.textContent = '';
  
  // Disable process button
  processButton.disabled = true;
  processButton.innerHTML = '<i class="bi bi-cpu me-2"></i>Process Meeting';
  
  // Reset upload zone opacity
  uploadZone.style.opacity = '1';
  
  // Clear file info
  fileName.textContent = '';
  fileSize.textContent = '';
  fileDuration.textContent = '';
}

// ============================================
// 10. INITIALIZE ON PAGE LOAD
// ============================================

/**
 * Initialize the upload handler when DOM is ready
 * Set up event listeners and initial states
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log('📤 Upload handler initialized');
  
  // Set initial button state
  if (processButton) {
    processButton.disabled = true;
  }
  
  // Add click listener to process button
  if (processButton) {
    processButton.addEventListener('click', simulateUpload);
  }
  
  // Add click listener to remove file button
  if (removeFileButton) {
    removeFileButton.addEventListener('click', removeFile);
  }
  
  // Prevent file input click event from bubbling to upload zone
  if (fileInput) {
    fileInput.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  }
  
  // Check if there's a previous upload to clear
  // (useful if user navigates back)
  if (localStorage.getItem('currentMeeting')) {
    // Keep it for the processing page
    console.log('📝 Previous meeting data found');
  }
  
  console.log('✅ All event listeners attached');
  console.log('📋 Supported formats: MP3, WAV, M4A');
  console.log('📏 Max file size: 100MB');
});

// ============================================
// ADDITIONAL UTILITY FUNCTIONS
// ============================================

/**
 * Format timestamp to readable date string
 * @param {string} isoString - ISO date string
 * @returns {string} - Formatted date
 */
function formatTimestamp(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Show error message to user
 * @param {string} message - Error message
 */
function showError(message) {
  // Create or update error alert
  let errorAlert = document.getElementById('errorAlert');
  
  if (!errorAlert) {
    errorAlert = document.createElement('div');
    errorAlert.id = 'errorAlert';
    errorAlert.className = 'alert alert-danger alert-dismissible fade show';
    errorAlert.innerHTML = `
      <i class="bi bi-exclamation-triangle me-2"></i>
      <span id="errorMessage"></span>
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert before upload zone
    uploadZone.parentNode.insertBefore(errorAlert, uploadZone);
  }
  
  document.getElementById('errorMessage').textContent = message;
  errorAlert.classList.add('slide-down');
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    errorAlert.classList.remove('show');
  }, 5000);
}

/**
 * Show success message to user
 * @param {string} message - Success message
 */
function showSuccess(message) {
  // Create or update success alert
  let successAlert = document.getElementById('successAlert');
  
  if (!successAlert) {
    successAlert = document.createElement('div');
    successAlert.id = 'successAlert';
    successAlert.className = 'alert alert-success alert-dismissible fade show';
    successAlert.innerHTML = `
      <i class="bi bi-check-circle me-2"></i>
      <span id="successMessage"></span>
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert before upload zone
    uploadZone.parentNode.insertBefore(successAlert, uploadZone);
  }
  
  document.getElementById('successMessage').textContent = message;
  successAlert.classList.add('slide-down');
  
  // Auto-hide after 3 seconds
  setTimeout(() => {
    successAlert.classList.remove('show');
  }, 3000);
}

// ============================================
// CONSOLE BANNER
// ============================================
console.log('%c📤 Meeting Summarizer - Upload Module', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cVersion 1.0.0', 'color: #764ba2; font-size: 12px;');
console.log('%cReady to process your meetings! 🚀', 'color: #10b981; font-size: 12px;');
