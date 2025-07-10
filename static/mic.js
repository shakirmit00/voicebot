let isListening = false;
let chatInterval = null;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDiv = document.getElementById("status");
const chatDiv = document.getElementById("chat-log");

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

const WAKE_WORDS = ["hi jarvis", "hey jarvis", "ok jarvis"];
const STOP_WORDS = ["stop jarvis", "cancel", "stop"];

function enableButtons() {
    startBtn.disabled = false;
    stopBtn.disabled = true;
}
function disableButtons() {
    startBtn.disabled = true;
    stopBtn.disabled = false;
}

disableButtons(); // Initially only start is enabled

startBtn.onclick = () => {
    statusDiv.innerText = "🎤 Say 'Hi Jarvis' to start...";
    recognition.start();
};

stopBtn.onclick = () => {
    stopListening();
};

function startListening() {
    isListening = true;
    disableButtons();
    statusDiv.innerText = "🎤 Listening...";
    fetch("/start", { method: "POST" });
    if (!chatInterval) {
        chatInterval = setInterval(fetchChat, 2000);
    }
}

function stopListening() {
    isListening = false;
    enableButtons();
    statusDiv.innerText = "🛑 Chat stopped";
    fetch("/stop", { method: "POST" });
    if (chatInterval) {
        clearInterval(chatInterval);
        chatInterval = null;
    }
    recognition.stop();
}

recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript.toLowerCase().trim();
    chatDiv.innerHTML += `<div><b>You:</b> ${transcript}</div>`;

    // Wake word detection
    if (!isListening && WAKE_WORDS.some(w => transcript.includes(w))) {
        statusDiv.innerText = "✅ Jarvis Activated!";
        startListening();
        speak("Hello, I am Jarvis. How can I help you?");
        setTimeout(() => recognition.start(), 1000);
        return;
    }
    // If not listening, ignore everything except wake word
    if (!isListening) {
        statusDiv.innerText = "❌ Please say 'Hi Jarvis' to begin.";
        setTimeout(() => recognition.start(), 1500);
        return;
    }
    // Stop word detection
    if (STOP_WORDS.some(w => transcript.includes(w))) {
        speak("Okay, stopping now.");
        stopListening();
        return;
    }
    statusDiv.innerText = "🤖 Thinking...";
    fetch("/voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: transcript }),
    })
    .then(res => res.json())
    .then(data => {
        const reply = data.reply;
        chatDiv.innerHTML += `<div><b>Jarvis:</b> ${reply}</div>`;
        // If backend provides audio_url, play it
        if (data.audio_url) {
            const audio = new Audio(data.audio_url);
            audio.play();
        } else {
            speak(reply);
        }
    })
    .catch(err => {
        chatDiv.innerHTML += `<div><b>Jarvis:</b> Sorry, something went wrong.</div>`;
    })
    .finally(() => {
        if (isListening) setTimeout(() => recognition.start(), 1000);
    });
};

recognition.onend = () => {
    if (!isListening) return;
    recognition.start();
};

function fetchChat() {
    fetch("/history")
        .then(res => res.json())
        .then(history => {
            chatDiv.innerHTML = history.map(msg =>
                `<div><b>${msg.role}:</b> ${msg.content}</div>`
            ).join("");
        });
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}
