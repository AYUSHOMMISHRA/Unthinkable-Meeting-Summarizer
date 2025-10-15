/* ============================================
   MEETING SUMMARIZER - RESULTS PAGE
   Interactive Features for Meeting Results
   ============================================ */

// ============================================
// GLOBAL VARIABLES
// ============================================
let meetingId = null;
let checkboxStates = {};

// ============================================
// 1. TAB SWITCHING FUNCTIONALITY
// ============================================

/**
 * Initialize tab switching functionality
 * Handles tab clicks and content display
 */
function initializeTabs() {
  // Get all tab buttons and content divs
  const tabButtons = document.querySelectorAll('.nav-link');
  const tabContents = document.querySelectorAll('.tab-pane');
  
  // Add click listener to each tab button
  tabButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Get target tab from data attribute or href
      const targetTab = button.getAttribute('data-bs-target') || button.getAttribute('href');
      
      // Remove 'active' class from all tabs and content
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => {
        content.classList.remove('show', 'active');
      });
      
      // Add 'active' class to clicked tab
      button.classList.add('active');
      
      // Show corresponding content with smooth transition
      const targetContent = document.querySelector(targetTab);
      if (targetContent) {
        targetContent.classList.add('show', 'active', 'fade-in');
        
        // Smooth scroll to content on mobile
        if (window.innerWidth < 768) {
          targetContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
      
      // Store active tab in localStorage
      localStorage.setItem('activeTab', targetTab);
    });
  });
  
  // Restore last active tab from localStorage
  const lastActiveTab = localStorage.getItem('activeTab');
  if (lastActiveTab) {
    const tabButton = document.querySelector(`[data-bs-target="${lastActiveTab}"], [href="${lastActiveTab}"]`);
    if (tabButton) {
      tabButton.click();
    }
  }
}

// ============================================
// 2. COPY TO CLIPBOARD FUNCTION
// ============================================

/**
 * Copy text content to clipboard with fallback
 * Shows toast notification on success
 * 
 * @param {string} elementId - ID of element containing text to copy
 * @param {string} customMessage - Optional custom success message
 */
async function copyToClipboard(elementId, customMessage = null) {
  const element = document.getElementById(elementId);
  
  if (!element) {
    console.error(`Element with ID '${elementId}' not found`);
    showToast('❌ Copy failed', 'danger');
    return;
  }
  
  // Get text content from element
  let textToCopy = element.innerText || element.textContent;
  
  // Clean up text (remove extra whitespace)
  textToCopy = textToCopy.trim();
  
  try {
    // Modern clipboard API (preferred method)
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(textToCopy);
      showToast(customMessage || '✅ Copied to clipboard!', 'success');
    } else {
      // Fallback for older browsers using execCommand
      copyToClipboardFallback(textToCopy);
      showToast(customMessage || '✅ Copied to clipboard!', 'success');
    }
  } catch (err) {
    console.error('Failed to copy:', err);
    // Try fallback method
    try {
      copyToClipboardFallback(textToCopy);
      showToast(customMessage || '✅ Copied to clipboard!', 'success');
    } catch (fallbackErr) {
      console.error('Fallback copy also failed:', fallbackErr);
      showToast('❌ Failed to copy', 'danger');
    }
  }
}

/**
 * Fallback clipboard copy using execCommand
 * For older browsers that don't support navigator.clipboard
 * 
 * @param {string} text - Text to copy
 */
function copyToClipboardFallback(text) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.left = '-999999px';
  textArea.style.top = '-999999px';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  
  try {
    const successful = document.execCommand('copy');
    if (!successful) {
      throw new Error('execCommand failed');
    }
  } finally {
    document.body.removeChild(textArea);
  }
}

// ============================================
// 3. COPY BUTTONS FOR EACH SECTION
// ============================================

/**
 * Initialize copy buttons for all sections
 */
function initializeCopyButtons() {
  // Copy Transcript button
  const copyTranscriptBtn = document.getElementById('copyTranscript');
  if (copyTranscriptBtn) {
    copyTranscriptBtn.addEventListener('click', () => {
      copyToClipboard('transcriptContent', '✅ Transcript copied!');
      animateButtonSuccess(copyTranscriptBtn);
    });
  }
  
  // Copy Summary button
  const copySummaryBtn = document.getElementById('copySummary');
  if (copySummaryBtn) {
    copySummaryBtn.addEventListener('click', () => {
      copyToClipboard('summaryContent', '✅ Summary copied!');
      animateButtonSuccess(copySummaryBtn);
    });
  }
  
  // Copy Action Items button
  const copyActionItemsBtn = document.getElementById('copyActionItems');
  if (copyActionItemsBtn) {
    copyActionItemsBtn.addEventListener('click', () => {
      copyToClipboard('actionItemsContent', '✅ Action items copied!');
      animateButtonSuccess(copyActionItemsBtn);
    });
  }
  
  // Copy All button
  const copyAllBtn = document.getElementById('copyAll');
  if (copyAllBtn) {
    copyAllBtn.addEventListener('click', () => {
      copyAllContent();
      animateButtonSuccess(copyAllBtn);
    });
  }
}

/**
 * Copy all content (transcript + summary + action items)
 */
function copyAllContent() {
  const transcript = document.getElementById('transcriptContent')?.innerText || '';
  const summary = document.getElementById('summaryContent')?.innerText || '';
  const actionItems = document.getElementById('actionItemsContent')?.innerText || '';
  
  const allContent = `
=== MEETING TRANSCRIPT ===
${transcript}

=== MEETING SUMMARY ===
${summary}

=== ACTION ITEMS ===
${actionItems}
  `.trim();
  
  navigator.clipboard.writeText(allContent)
    .then(() => {
      showToast('✅ All content copied!', 'success');
    })
    .catch(() => {
      showToast('❌ Failed to copy', 'danger');
    });
}

/**
 * Animate button to show success feedback
 * Temporarily changes icon and color
 * 
 * @param {HTMLElement} button - Button element to animate
 */
function animateButtonSuccess(button) {
  const originalHTML = button.innerHTML;
  const originalClass = button.className;
  
  // Change to success state
  button.innerHTML = '<i class="bi bi-check-circle me-2"></i>Copied!';
  button.classList.add('btn-success');
  button.disabled = true;
  
  // Revert after 2 seconds
  setTimeout(() => {
    button.innerHTML = originalHTML;
    button.className = originalClass;
    button.disabled = false;
  }, 2000);
}

// ============================================
// 4. ACTION ITEM CHECKBOX TOGGLE
// ============================================

/**
 * Initialize action item checkboxes
 * Handles checkbox state changes and persistence
 */
function initializeActionItemCheckboxes() {
  const checkboxes = document.querySelectorAll('.action-item-checkbox');
  
  checkboxes.forEach(checkbox => {
    // Add change event listener
    checkbox.addEventListener('change', (e) => {
      handleCheckboxChange(e.target);
    });
  });
  
  // Load saved states
  loadCheckboxStates();
  updateCompletionPercentage();
}

/**
 * Handle checkbox state change
 * Adds strikethrough and saves state
 * 
 * @param {HTMLInputElement} checkbox - Checkbox element
 */
function handleCheckboxChange(checkbox) {
  const row = checkbox.closest('tr');
  const taskCell = row?.querySelector('td:nth-child(2)');
  
  if (taskCell) {
    if (checkbox.checked) {
      // Add strikethrough style
      taskCell.style.textDecoration = 'line-through';
      taskCell.style.opacity = '0.6';
    } else {
      // Remove strikethrough style
      taskCell.style.textDecoration = 'none';
      taskCell.style.opacity = '1';
    }
  }
  
  // Save state to localStorage
  saveCheckboxState(checkbox);
  
  // Update completion percentage
  updateCompletionPercentage();
  
  // Show feedback
  if (checkbox.checked) {
    showToast('✅ Task marked as complete', 'success');
  }
}

/**
 * Save checkbox state to localStorage
 * 
 * @param {HTMLInputElement} checkbox - Checkbox element
 */
function saveCheckboxState(checkbox) {
  const checkboxId = checkbox.id || checkbox.getAttribute('data-task-id');
  
  if (checkboxId) {
    checkboxStates[checkboxId] = checkbox.checked;
    localStorage.setItem('actionItemStates', JSON.stringify(checkboxStates));
  }
}

/**
 * Load saved checkbox states from localStorage
 */
function loadCheckboxStates() {
  // Get saved states from localStorage
  const savedStates = localStorage.getItem('actionItemStates');
  
  if (savedStates) {
    checkboxStates = JSON.parse(savedStates);
    
    // Apply saved states to checkboxes
    Object.keys(checkboxStates).forEach(checkboxId => {
      const checkbox = document.getElementById(checkboxId) || 
                      document.querySelector(`[data-task-id="${checkboxId}"]`);
      
      if (checkbox) {
        checkbox.checked = checkboxStates[checkboxId];
        
        // Apply visual state
        if (checkbox.checked) {
          const row = checkbox.closest('tr');
          const taskCell = row?.querySelector('td:nth-child(2)');
          
          if (taskCell) {
            taskCell.style.textDecoration = 'line-through';
            taskCell.style.opacity = '0.6';
          }
        }
      }
    });
  }
}

/**
 * Update action items completion percentage
 */
function updateCompletionPercentage() {
  const checkboxes = document.querySelectorAll('.action-item-checkbox');
  const total = checkboxes.length;
  const completed = Array.from(checkboxes).filter(cb => cb.checked).length;
  
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
  
  // Update percentage display if element exists
  const percentageElement = document.getElementById('completionPercentage');
  if (percentageElement) {
    percentageElement.textContent = `${percentage}%`;
  }
  
  // Update progress bar if exists
  const progressBar = document.getElementById('completionProgressBar');
  if (progressBar) {
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute('aria-valuenow', percentage);
  }
  
  // Update count display
  const countElement = document.getElementById('completionCount');
  if (countElement) {
    countElement.textContent = `${completed} of ${total} tasks completed`;
  }
}

// ============================================
// 5. DOWNLOAD PDF FUNCTION
// ============================================

/**
 * Download meeting results as PDF
 * Currently uses browser print dialog
 * Future: Implement server-side PDF generation
 */
function downloadPDF() {
  // Show loading toast
  showToast('📄 Preparing PDF...', 'info');
  
  // Option 1: Use browser print dialog (current implementation)
  setTimeout(() => {
    window.print();
  }, 500);
  
  // Option 2: Show coming soon message (alternative)
  // showToast('📄 PDF download feature coming soon!', 'warning');
  
  // Future implementation would call server endpoint:
  // fetch('/api/meeting/{id}/pdf')
  //   .then(response => response.blob())
  //   .then(blob => {
  //     const url = window.URL.createObjectURL(blob);
  //     const a = document.createElement('a');
  //     a.href = url;
  //     a.download = 'meeting-summary.pdf';
  //     a.click();
  //   });
}

// ============================================
// 6. SHARE LINK FUNCTION
// ============================================

/**
 * Share meeting link by copying URL to clipboard
 * Shows toast notification on success
 */
function shareLink() {
  const currentUrl = window.location.href;
  
  navigator.clipboard.writeText(currentUrl)
    .then(() => {
      showToast('🔗 Link copied to clipboard!', 'success');
    })
    .catch(() => {
      // Fallback
      try {
        copyToClipboardFallback(currentUrl);
        showToast('🔗 Link copied to clipboard!', 'success');
      } catch (err) {
        showToast('❌ Failed to copy link', 'danger');
      }
    });
}

// ============================================
// 7. DELETE MEETING FUNCTION
// ============================================

/**
 * Delete current meeting with confirmation
 * Shows loading state and redirects on success
 */
function deleteMeeting() {
  // Show confirmation dialog
  const confirmed = confirm(
    '⚠️ Are you sure you want to delete this meeting?\n\n' +
    'This action cannot be undone. All transcripts, summaries, and action items will be permanently deleted.'
  );
  
  if (!confirmed) {
    return;
  }
  
  // Get delete button
  const deleteBtn = document.getElementById('deleteButton');
  
  if (deleteBtn) {
    // Show loading state
    const originalHTML = deleteBtn.innerHTML;
    deleteBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Deleting...';
    deleteBtn.disabled = true;
  }
  
  // Show loading toast
  showToast('🗑️ Deleting meeting...', 'info');
  
  // Simulate deletion (replace with actual API call)
  setTimeout(() => {
    // Clear localStorage
    localStorage.removeItem('currentMeeting');
    localStorage.removeItem('actionItemStates');
    
    // Show success message
    showToast('✅ Meeting deleted successfully!', 'success');
    
    // Redirect to meetings list after short delay
    setTimeout(() => {
      window.location.href = '/meetings';
    }, 1000);
  }, 1500);
  
  // Future implementation with API:
  // fetch(`/api/meeting/${meetingId}`, { method: 'DELETE' })
  //   .then(response => {
  //     if (response.ok) {
  //       showToast('✅ Meeting deleted!', 'success');
  //       window.location.href = '/meetings';
  //     } else {
  //       throw new Error('Delete failed');
  //     }
  //   })
  //   .catch(err => {
  //     showToast('❌ Failed to delete meeting', 'danger');
  //     deleteBtn.innerHTML = originalHTML;
  //     deleteBtn.disabled = false;
  //   });
}

// ============================================
// 8. TOAST NOTIFICATION SYSTEM
// ============================================

/**
 * Show toast notification
 * Creates toast dynamically, displays for 3 seconds, then removes
 * 
 * @param {string} message - Toast message
 * @param {string} type - Toast type: 'success', 'danger', 'warning', 'info'
 */
function showToast(message, type = 'info') {
  // Create toast container if it doesn't exist
  let toastContainer = document.getElementById('toastContainer');
  
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toastContainer';
    toastContainer.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(toastContainer);
  }
  
  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast-notification toast-${type}`;
  
  // Set background color based on type
  const colors = {
    success: 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)',
    danger: 'linear-gradient(135deg, #f87171 0%, #ef4444 100%)',
    warning: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
    info: 'linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)'
  };
  
  toast.style.cssText = `
    background: ${colors[type] || colors.info};
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    font-weight: 500;
    min-width: 250px;
    max-width: 400px;
    animation: slideInRight 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
  `;
  
  toast.innerHTML = `
    <span style="font-size: 16px;">${message}</span>
  `;
  
  // Add to container
  toastContainer.appendChild(toast);
  
  // Fade in
  setTimeout(() => {
    toast.style.opacity = '1';
  }, 10);
  
  // Remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    
    setTimeout(() => {
      toast.remove();
      
      // Remove container if empty
      if (toastContainer.children.length === 0) {
        toastContainer.remove();
      }
    }, 300);
  }, 3000);
}

// Add toast animations to document
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOutRight {
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

// ============================================
// 9. SMOOTH SCROLL TO TABS
// ============================================

/**
 * Smooth scroll to tab content when clicked
 * Especially useful on mobile devices
 */
function enableSmoothScrollToTabs() {
  const tabButtons = document.querySelectorAll('.nav-link');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      // On mobile, scroll to tab content
      if (window.innerWidth < 768) {
        const targetTab = button.getAttribute('data-bs-target') || button.getAttribute('href');
        const targetContent = document.querySelector(targetTab);
        
        if (targetContent) {
          setTimeout(() => {
            targetContent.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }, 100);
        }
      }
    });
  });
}

// ============================================
// ADDITIONAL UTILITY FUNCTIONS
// ============================================

/**
 * Export meeting data as JSON
 */
function exportAsJSON() {
  const meetingData = {
    title: document.querySelector('h1')?.textContent || 'Meeting Summary',
    date: document.querySelector('.meeting-date')?.textContent || new Date().toLocaleDateString(),
    transcript: document.getElementById('transcriptContent')?.innerText || '',
    summary: document.getElementById('summaryContent')?.innerText || '',
    actionItems: document.getElementById('actionItemsContent')?.innerText || '',
    exportedAt: new Date().toISOString()
  };
  
  const dataStr = JSON.stringify(meetingData, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = 'meeting-summary.json';
  link.click();
  
  URL.revokeObjectURL(url);
  showToast('✅ Exported as JSON', 'success');
}

/**
 * Print meeting summary
 */
function printMeeting() {
  window.print();
}

/**
 * Toggle transcript font size
 */
function toggleTranscriptFontSize() {
  const transcript = document.getElementById('transcriptContent');
  if (transcript) {
    transcript.classList.toggle('large-font');
  }
}

// ============================================
// 10. INITIALIZE ON PAGE LOAD
// ============================================

/**
 * Initialize all interactive features when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log('📊 Results page initialized');
  
  // Initialize tab switching
  initializeTabs();
  
  // Initialize copy buttons
  initializeCopyButtons();
  
  // Initialize action item checkboxes
  initializeActionItemCheckboxes();
  
  // Enable smooth scroll to tabs
  enableSmoothScrollToTabs();
  
  // Attach event listeners to action buttons
  const downloadPDFBtn = document.getElementById('downloadPDF');
  if (downloadPDFBtn) {
    downloadPDFBtn.addEventListener('click', downloadPDF);
  }
  
  const shareBtn = document.getElementById('shareButton');
  if (shareBtn) {
    shareBtn.addEventListener('click', shareLink);
  }
  
  const deleteBtn = document.getElementById('deleteButton');
  if (deleteBtn) {
    deleteBtn.addEventListener('click', deleteMeeting);
  }
  
  // Load meeting data from localStorage if available
  const meetingData = localStorage.getItem('currentMeeting');
  if (meetingData) {
    console.log('📝 Meeting data loaded from localStorage');
  }
  
  console.log('✅ All interactive features initialized');
  console.log('📋 Features: Tabs, Copy, Checkboxes, Share, Delete, PDF');
});

// ============================================
// CONSOLE BANNER
// ============================================
console.log('%c📊 Meeting Summarizer - Results Module', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cVersion 1.0.0', 'color: #764ba2; font-size: 12px;');
console.log('%cInteractive results page ready! 🚀', 'color: #10b981; font-size: 12px;');
