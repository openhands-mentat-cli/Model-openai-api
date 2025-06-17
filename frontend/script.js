// Global variables
let currentTab = 'chat';
let isTyping = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateBaseUrls();
    checkHealth();
    loadModels();
    showTab('chat');
});

// Update base URLs in documentation
function updateBaseUrls() {
    const baseUrl = window.location.origin;
    const pythonElement = document.getElementById('base-url-python');
    const curlElement = document.getElementById('base-url-curl');
    
    if (pythonElement) pythonElement.textContent = baseUrl;
    if (curlElement) curlElement.textContent = baseUrl;
}

// Tab switching
function showTab(tabName) {
    // Hide all content divs
    document.getElementById('chat-content').classList.add('hidden');
    document.getElementById('docs-content').classList.add('hidden');
    document.getElementById('status-content').classList.add('hidden');
    
    // Remove active class from all tabs
    document.getElementById('chat-tab').classList.remove('bg-blue-700');
    document.getElementById('docs-tab').classList.remove('bg-blue-700');
    document.getElementById('status-tab').classList.remove('bg-blue-700');
    
    // Show selected content and activate tab
    document.getElementById(tabName + '-content').classList.remove('hidden');
    document.getElementById(tabName + '-tab').classList.add('bg-blue-700');
    
    currentTab = tabName;
    
    // Refresh data for certain tabs
    if (tabName === 'status') {
        checkHealth();
        loadModels();
    }
}

// Chat functionality
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message || isTyping) return;
    
    // Clear input and disable send button
    input.value = '';
    setSendButtonState(false);
    
    // Add user message
    addMessage('user', message);
    
    // Add typing indicator
    const typingId = addTypingIndicator();
    
    try {
        isTyping = true;
        const response = await fetch('/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer $$Hello1$$',
            },
            body: JSON.stringify({
                model: 'phi-3-mini-128k',
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ],
                max_tokens: 1000,
                temperature: 0.7,
                stream: false
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant response
        if (data.choices && data.choices[0] && data.choices[0].message) {
            addMessage('assistant', data.choices[0].message.content);
        } else {
            addMessage('assistant', 'Sorry, I encountered an error processing your request.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        addMessage('assistant', `Error: ${error.message}. Please check if the server is running.`);
    } finally {
        isTyping = false;
        setSendButtonState(true);
    }
}

function addMessage(role, content) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';
    
    const isUser = role === 'user';
    const iconClass = isUser ? 'fas fa-user' : 'fas fa-robot';
    const bgColor = isUser ? 'bg-gray-100' : 'bg-blue-50';
    const iconBg = isUser ? 'bg-gray-600' : 'bg-blue-600';
    const justify = isUser ? 'justify-end' : 'justify-start';
    
    messageDiv.innerHTML = `
        <div class="flex items-start space-x-3 ${justify}">
            ${!isUser ? `
                <div class="${iconBg} text-white rounded-full w-8 h-8 flex items-center justify-center">
                    <i class="${iconClass} text-sm"></i>
                </div>
            ` : ''}
            <div class="${bgColor} rounded-lg p-3 max-w-md">
                <p class="text-gray-800 whitespace-pre-wrap">${escapeHtml(content)}</p>
            </div>
            ${isUser ? `
                <div class="${iconBg} text-white rounded-full w-8 h-8 flex items-center justify-center">
                    <i class="${iconClass} text-sm"></i>
                </div>
            ` : ''}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'chat-message typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="flex items-start space-x-3">
            <div class="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center">
                <i class="fas fa-robot text-sm"></i>
            </div>
            <div class="bg-blue-50 rounded-lg p-3">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
        typingDiv.remove();
    }
}

function setSendButtonState(enabled) {
    const sendButton = document.getElementById('send-button');
    sendButton.disabled = !enabled;
    if (enabled) {
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    } else {
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }
}

// API Testing
async function testAPI() {
    const input = document.getElementById('api-test-input');
    const button = document.getElementById('test-api-button');
    const resultDiv = document.getElementById('api-test-result');
    const responseText = document.getElementById('api-response-text');
    
    const message = input.value.trim();
    if (!message) return;
    
    // Disable button and show loading
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Testing...';
    
    try {
        const response = await fetch('/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer $$Hello1$$',
            },
            body: JSON.stringify({
                model: 'phi-3-mini-128k',
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ],
                max_tokens: 200,
                temperature: 0.7
            })
        });
        
        const data = await response.json();
        
        // Show result
        responseText.textContent = JSON.stringify(data, null, 2);
        resultDiv.classList.remove('hidden');
        
    } catch (error) {
        responseText.textContent = `Error: ${error.message}`;
        resultDiv.classList.remove('hidden');
    } finally {
        // Re-enable button
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-play mr-2"></i>Test API';
    }
}

// Health check
async function checkHealth() {
    const indicator = document.getElementById('health-indicator');
    const text = document.getElementById('health-text');
    
    try {
        const response = await fetch('/health');
        
        if (response.ok) {
            indicator.className = 'w-3 h-3 rounded-full mr-3 bg-green-500';
            text.textContent = 'Server is healthy';
        } else {
            indicator.className = 'w-3 h-3 rounded-full mr-3 bg-yellow-500';
            text.textContent = `Server responded with status ${response.status}`;
        }
    } catch (error) {
        indicator.className = 'w-3 h-3 rounded-full mr-3 bg-red-500';
        text.textContent = 'Server is unreachable';
    }
}

// Load models
async function loadModels() {
    const modelsDiv = document.getElementById('models-list');
    
    try {
        const response = await fetch('/v1/models', {
            headers: {
                'Authorization': 'Bearer $$Hello1$$'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.data && data.data.length > 0) {
                modelsDiv.innerHTML = data.data.map(model => `
                    <div class="border-b border-gray-200 py-2 last:border-b-0">
                        <div class="font-medium">${model.id}</div>
                        <div class="text-sm text-gray-600">Object: ${model.object}</div>
                    </div>
                `).join('');
            } else {
                modelsDiv.innerHTML = '<div class="text-gray-600">No models available</div>';
            }
        } else {
            modelsDiv.innerHTML = '<div class="text-red-600">Failed to load models</div>';
        }
    } catch (error) {
        modelsDiv.innerHTML = '<div class="text-red-600">Error loading models</div>';
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
