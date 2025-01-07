document.getElementById('send-btn').addEventListener('click', function() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() === "") return;

    // Display user message
    var userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.textContent = userInput;
    document.getElementById('conversation').appendChild(userMessageDiv);

    // Clear input field
    document.getElementById('user-input').value = "";

    // Send the message to the backend
    fetch('/get_response', {
        method: 'POST',
        body: new URLSearchParams({
            'message': userInput
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        var botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'bot-message';
        botMessageDiv.textContent = data.response;
        document.getElementById('conversation').appendChild(botMessageDiv);
    });
});

// Handle FAQ question click
document.querySelectorAll('.faq-question').forEach(function(faqElement) {
    faqElement.addEventListener('click', function() {
        var question = faqElement.getAttribute('data-question');
        
        // Display the question as user input
        var userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'user-message';
        userMessageDiv.textContent = question;
        document.getElementById('conversation').appendChild(userMessageDiv);

        // Send the FAQ question to the backend
        fetch('/get_response', {
            method: 'POST',
            body: new URLSearchParams({
                'message': question
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            var botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'bot-message';
            botMessageDiv.textContent = data.response;
            document.getElementById('conversation').appendChild(botMessageDiv);
        });
    });
});