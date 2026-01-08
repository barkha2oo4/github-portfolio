document.getElementById('query-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const input = document.getElementById('user-input').value;
    const responseDiv = document.getElementById('response');
    responseDiv.textContent = 'Thinking...';
    const res = await fetch('/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input })
    });
    const data = await res.json();
    // Render HTML (with bold, line breaks)
    // Wrap response in a chat bubble
    responseDiv.innerHTML = `<div class="assistant-bubble">${data.response}</div>`;
    window.lastAssistantResponse = responseDiv.textContent;
});

// TTS: Speak the response when button is clicked
const ttsBtn = document.getElementById('tts-btn');
ttsBtn.addEventListener('click', function() {
    if (window.lastAssistantResponse) {
        const synth = window.speechSynthesis;
        synth.speak(new SpeechSynthesisUtterance(window.lastAssistantResponse));
    }
});

// Speech-to-text: Use browser microphone
const micBtn = document.getElementById('mic-btn');
if (window.webkitSpeechRecognition || window.SpeechRecognition) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    micBtn.addEventListener('click', function() {
        recognition.start();
    });
    recognition.onresult = function(e) {
        document.getElementById('user-input').value = e.results[0][0].transcript;
    };
    recognition.onerror = function(e) {
        alert('Speech recognition error: ' + e.error);
    };
} else {
    micBtn.disabled = true;
    micBtn.title = 'Speech recognition not supported in this browser.';
}
