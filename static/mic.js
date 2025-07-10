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

document.addEventListener("DOMContentLoaded", function() {
    const startBtn = document.getElementById("startBtn");
    const stopBtn = document.getElementById("stopBtn");
    const statusDiv = document.getElementById("status");
    const chatDiv = document.getElementById("chat-log");

    if (!startBtn || !stopBtn || !statusDiv || !chatDiv) {
        console.error("DOM elements not found for mic.js");
        return;
    }

    function startListening() {
        isListening = true;
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusDiv.innerText = "🎤 Say something...";
        recognition.start();
        fetch("/start", { method: "POST" });
        if (!chatInterval) {
            chatInterval = setInterval(fetchChat, 2000);
        }
    }

    function stopListening() {
        isListening = false;
        recognition.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusDiv.innerText = "🛑 Chat stopped";
        fetch("/stop", { method: "POST" });
        if (chatInterval) {
            clearInterval(chatInterval);
            chatInterval = null;
        }
    }

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        chatDiv.innerHTML += `<div><b>You:</b> ${transcript}</div>`;
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
            speak(reply);
        })
        .catch(err => {
            chatDiv.innerHTML += `<div><b>Jarvis:</b> Sorry, something went wrong.</div>`;
        })
        .finally(() => {
            if (isListening) setTimeout(() => recognition.start(), 1000);
        });
    };

    recognition.onend = () => {
        if (isListening) recognition.start();
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

    window.startListening = startListening;
    window.stopListening = stopListening;
});
