/**
 * Custom JavaScript to fix cross-origin messaging issues
 * for the AI Travel Assistant application
 */

// Override postMessage to use the correct origin
(function() {
    // Store the original postMessage function
    const originalPostMessage = window.postMessage;
    
    // Override postMessage to use dynamic origin
    window.postMessage = function(message, targetOrigin, transfer) {
        // Use the current window's origin instead of hardcoded origins
        const currentOrigin = window.location.origin;
        
        // Call the original with the correct origin
        return originalPostMessage.call(this, message, currentOrigin, transfer);
    };
    
    // Listen for DOMContentLoaded to initialize
    document.addEventListener('DOMContentLoaded', function() {
        console.log('AI Travel Assistant custom scripts initialized');
        
        // Fix any autofocus issues by ensuring only one element has focus
        setTimeout(function() {
            const autofocusElements = document.querySelectorAll('[autofocus]');
            if (autofocusElements.length > 1) {
                // Keep only the first autofocus element
                for (let i = 1; i < autofocusElements.length; i++) {
                    autofocusElements[i].removeAttribute('autofocus');
                }
            }
        }, 500);
    });
})();
