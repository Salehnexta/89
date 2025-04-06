/**
 * Connection management for the AI Travel Assistant
 * Handles reconnection and error recovery
 */

(function() {
    // Track connection status
    let connectionStatus = {
        connected: true,
        reconnectAttempts: 0,
        maxReconnectAttempts: 5,
        reconnectDelay: 2000 // Start with 2 seconds
    };

    // Function to check server connection
    function checkConnection() {
        const apiUrl = window.location.origin + '/gradio_api/heartbeat';
        
        fetch(apiUrl, { 
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            cache: 'no-store'
        })
        .then(response => {
            if (response.ok) {
                // Connection restored
                if (!connectionStatus.connected) {
                    console.log('Connection restored');
                    connectionStatus.connected = true;
                    connectionStatus.reconnectAttempts = 0;
                    connectionStatus.reconnectDelay = 2000;
                    
                    // Remove any error messages
                    const errorBanner = document.getElementById('connection-error');
                    if (errorBanner) {
                        errorBanner.remove();
                    }
                }
            } else {
                handleConnectionError('Server returned error status');
            }
        })
        .catch(error => {
            handleConnectionError(`Connection error: ${error.message}`);
        });
    }

    // Handle connection errors
    function handleConnectionError(errorMessage) {
        console.warn(errorMessage);
        
        if (connectionStatus.connected) {
            connectionStatus.connected = false;
            
            // Show error message to user
            showErrorBanner('Connection to server lost. Attempting to reconnect...');
        }
        
        // Attempt reconnection with exponential backoff
        if (connectionStatus.reconnectAttempts < connectionStatus.maxReconnectAttempts) {
            connectionStatus.reconnectAttempts++;
            connectionStatus.reconnectDelay *= 1.5; // Increase delay with each attempt
            
            console.log(`Reconnect attempt ${connectionStatus.reconnectAttempts} in ${Math.round(connectionStatus.reconnectDelay/1000)}s`);
            
            setTimeout(checkConnection, connectionStatus.reconnectDelay);
        } else {
            showErrorBanner('Unable to connect to server. Please refresh the page or check your connection.');
        }
    }

    // Show error banner
    function showErrorBanner(message) {
        // Remove existing banner if any
        const existingBanner = document.getElementById('connection-error');
        if (existingBanner) {
            existingBanner.remove();
        }
        
        // Create new banner
        const banner = document.createElement('div');
        banner.id = 'connection-error';
        banner.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; background-color: #f8d7da; color: #721c24; padding: 10px; text-align: center; z-index: 9999; font-family: sans-serif;';
        banner.textContent = message;
        
        // Add refresh button
        const refreshButton = document.createElement('button');
        refreshButton.textContent = 'Refresh Page';
        refreshButton.style.cssText = 'margin-left: 10px; padding: 5px 10px; background-color: #721c24; color: white; border: none; border-radius: 3px; cursor: pointer;';
        refreshButton.onclick = function() {
            window.location.reload();
        };
        
        banner.appendChild(refreshButton);
        document.body.appendChild(banner);
    }

    // Set up periodic connection checking
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Connection monitoring initialized');
        
        // Check connection every 30 seconds
        setInterval(checkConnection, 30000);
        
        // Override fetch to handle connection errors
        const originalFetch = window.fetch;
        window.fetch = function(url, options) {
            return originalFetch(url, options)
                .catch(error => {
                    // Only handle API calls to our backend
                    if (url.toString().includes('/gradio_api/') || 
                        url.toString().includes('/chat')) {
                        handleConnectionError(`Fetch error: ${error.message}`);
                    }
                    throw error;
                });
        };
    });
})();
