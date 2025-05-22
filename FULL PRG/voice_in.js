// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const micButton = document.getElementById('mic');
    const responseBox = document.getElementById('Aarav');

    // Initialize Speech Recognition
    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true; // Keep listening for speech
    recognition.lang = 'en-US'; // Set language to English (United States)

    // Event listener for mic button click
    micButton.addEventListener('click', function() {
        // Start speech recognition
        recognition.start();
    });

    // Event listener for speech recognition result
    recognition.onresult = function(event) {
        // Get the recognized text from the event
        const transcript = event.results[0][0].transcript;
        
        // Update the response box with the recognized text
        responseBox.textContent = transcript;
    };

    // Event listener for speech recognition error
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
});
