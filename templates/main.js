document.addEventListener('DOMContentLoaded', function() {
    const chatDisplay = document.getElementById('chat-display');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
  
    sendButton.addEventListener('click', function() {
      sendMessage();
    });
  
    userInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        sendMessage();
      }
    });
  
    function sendMessage() {
      const message = userInput.value.trim();
      if (message !== '') {
        displayUserMessage(message);
        sendRequestToBackend(message);
        userInput.value = '';
      }
    }
  
    function displayUserMessage(message) {
      const userMessage = document.createElement('div');
      userMessage.className = 'message user';
      userMessage.innerHTML = message;
      chatDisplay.appendChild(userMessage);
      chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }
  
    function displayBotMessage(message) {
      const botMessage = document.createElement('div');
      botMessage.className = 'message bot';
      botMessage.innerHTML = message;
      chatDisplay.appendChild(botMessage);
      chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }
  
    function sendRequestToBackend(message) {
      const request = new XMLHttpRequest();
      request.open('POST', '/chat', true);
      request.setRequestHeader('Content-Type', 'application/json');
  
      request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
          const response = JSON.parse(request.responseText);
          displayBotMessage(response.response);
        } else {
          console.error('Request failed. Status:', request.status);
        }
      };
  
      request.onerror = function() {
        console.error('Request failed');
      };
  
      const data = { message: message };
      request.send(JSON.stringify(data));
    }
  });
  