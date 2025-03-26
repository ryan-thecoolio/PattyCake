const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-btn');

function sendMessage() {
    const userMessage = userInput.value;
    if (userMessage.trim() !== '') {
        addMessage(userMessage, 'user');
        sendData(userMessage);
        userInput.value = '';
    }
}

sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

function addMessage(message, sender) {
    const chatbox = document.getElementById('chatbox');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.innerHTML = message;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendData(value) {
    $.ajax({
        url: '/process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'value': value }),
        success: function(response) {
            addMessage(response.result, 'bot');
        },
        error: function(error) {
            console.error(error);
            addMessage("Error communicating with server", 'bot');
        }
    });
}