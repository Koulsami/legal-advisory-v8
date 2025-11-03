// Legal Advisory System v8.0 - Frontend Application

// Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://your-backend-url.railway.app'; // Update this after Railway deployment

// State
let conversationHistory = [];
let isWaitingForResponse = false;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Legal Advisory System v8.0 loaded');
    checkSystemHealth();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Enter key to send (Shift+Enter for new line)
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send button click
    sendBtn.addEventListener('click', sendMessage);
}

// Check system health
async function checkSystemHealth() {
    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.dot');
    const modulesEl = document.getElementById('modules');

    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();

        if (data.status === 'healthy') {
            statusText.textContent = 'Online';
            statusDot.classList.remove('offline');

            // Display available modules
            if (data.modules && data.modules.length > 0) {
                modulesEl.textContent = data.modules.join(', ');
            } else {
                modulesEl.textContent = 'Loading...';
            }
        } else {
            throw new Error('System not healthy');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        statusText.textContent = 'Offline';
        statusDot.classList.add('offline');
        modulesEl.textContent = 'Unavailable';

        // Show error in chat
        addSystemMessage(
            'Unable to connect to backend API. Please check if the backend is running.',
            'error'
        );
    }
}

// Send message
async function sendMessage() {
    const input = document.getElementById('user-input');
    const question = input.value.trim();

    if (!question || isWaitingForResponse) {
        return;
    }

    // Clear input and disable
    input.value = '';
    setLoading(true);

    // Add user message to chat
    addMessage('user', question);

    try {
        const response = await fetch(`${API_BASE_URL}/api/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                conversation_history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Update conversation history
        conversationHistory.push({
            role: 'user',
            content: question
        });

        // Handle response based on type
        if (data.needs_clarification) {
            handleClarificationResponse(data);
        } else {
            handleDirectResponse(data);
        }

        // Add assistant response to history
        conversationHistory.push({
            role: 'assistant',
            content: data.answer || JSON.stringify(data.clarifying_questions)
        });

        // Keep only last 6 messages (3 turns)
        if (conversationHistory.length > 6) {
            conversationHistory = conversationHistory.slice(-6);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addSystemMessage(
            'Failed to get response from the server. Please try again.',
            'error'
        );
    } finally {
        setLoading(false);
    }
}

// Handle clarification response
function handleClarificationResponse(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';

    let html = `
        <div class="message-content">
            <p><strong>I need some more information to answer your question accurately.</strong></p>
            <div class="clarifying-questions">
                <h3>📋 CLARIFYING QUESTIONS:</h3>
                <ol>
    `;

    data.clarifying_questions.forEach(q => {
        html += `<li>${q}</li>`;
    });

    html += `
                </ol>
            </div>
            <div class="confidence-badge confidence-low">
                ⚠️ Confidence: ${Math.round(data.confidence * 100)}% (below 30% threshold)
            </div>
            <p style="margin-top: 15px;"><em>💡 TIP: You can answer one or more of these questions to help me provide a more accurate answer.</em></p>
        </div>
    `;

    messageDiv.innerHTML = html;

    const chatContainer = document.getElementById('chat-container');
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Handle direct response
function handleDirectResponse(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';

    let answer = data.answer || 'No answer provided';

    // Format the answer (preserve line breaks and structure)
    answer = formatAnswer(answer);

    // Determine confidence level
    const confidence = data.confidence || 0;
    let confidenceClass = 'confidence-low';
    if (confidence >= 0.7) {
        confidenceClass = 'confidence-high';
    } else if (confidence >= 0.4) {
        confidenceClass = 'confidence-medium';
    }

    const html = `
        <div class="message-content">
            ${answer}
            <div class="confidence-badge ${confidenceClass}">
                ✓ Confidence: ${Math.round(confidence * 100)}%
            </div>
        </div>
    `;

    messageDiv.innerHTML = html;

    const chatContainer = document.getElementById('chat-container');
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Format answer with proper structure
function formatAnswer(answer) {
    // Convert markdown-style formatting to HTML
    let formatted = answer
        // Bold text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic text
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Preserve line breaks
        .replace(/\n/g, '<br>');

    // Format case citations if present
    if (formatted.includes('📚') || formatted.includes('Case:') || formatted.includes('CASE LAW')) {
        formatted = formatCaseCitations(formatted);
    }

    return formatted;
}

// Format case citations
function formatCaseCitations(text) {
    // Split by case markers
    const parts = text.split(/(📚|Case:|CASE LAW REFERENCES:)/);
    let html = '';

    for (let i = 0; i < parts.length; i++) {
        const part = parts[i].trim();

        if (part === '📚' || part.includes('Case:') || part.includes('CASE LAW')) {
            // Start case citation block
            html += '<div class="case-citation">';
            html += '<div class="case-name">📚 ' + parts[i + 1] + '</div>';
            i++; // Skip next part as we already used it
        } else if (part.includes('REASONING') || part.includes('WHY')) {
            html += '<div class="reasoning"><strong>Reasoning Summary:</strong><br>' + part + '</div>';
        } else if (part.includes('VERBATIM') || part.includes('QUOTE')) {
            html += '<div class="quote"><strong>Verbatim Quote:</strong><br>' + part + '</div>';
            html += '</div>'; // Close case citation block
        } else if (part) {
            html += '<p>' + part + '</p>';
        }
    }

    return html;
}

// Add message to chat
function addMessage(role, content) {
    const chatContainer = document.getElementById('chat-container');

    // Remove welcome message if present
    const welcomeMsg = chatContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = content.replace(/\n/g, '<br>');

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

// Add system message
function addSystemMessage(content, type = 'info') {
    const chatContainer = document.getElementById('chat-container');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant';

    const iconMap = {
        'info': 'ℹ️',
        'error': '⚠️',
        'success': '✅'
    };

    const html = `
        <div class="message-content" style="background: ${type === 'error' ? '#f8d7da' : '#d1ecf1'}; border-color: ${type === 'error' ? '#f5c6cb' : '#bee5eb'}">
            ${iconMap[type]} ${content}
        </div>
    `;

    messageDiv.innerHTML = html;
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

// Set loading state
function setLoading(loading) {
    isWaitingForResponse = loading;
    const sendBtn = document.getElementById('send-btn');
    const btnText = document.getElementById('send-btn-text');
    const spinner = document.getElementById('send-btn-spinner');
    const input = document.getElementById('user-input');

    if (loading) {
        sendBtn.disabled = true;
        input.disabled = true;
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
    } else {
        sendBtn.disabled = false;
        input.disabled = false;
        btnText.classList.remove('hidden');
        spinner.classList.add('hidden');
        input.focus();
    }
}

// Set question from example button
function setQuestion(question) {
    const input = document.getElementById('user-input');
    input.value = question;
    input.focus();
}

// Scroll chat to bottom
function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Export for use in HTML onclick handlers
window.sendMessage = sendMessage;
window.setQuestion = setQuestion;
