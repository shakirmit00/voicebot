let isListening = false;
let isAwake = false;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDiv = document.getElementById("status");
const chatDiv = document.getElementById("chat");

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

function startListening() {
  isListening = true;
  isAwake = false;
  startBtn.disabled = true;
  stopBtn.disabled = false;
  statusDiv.innerText = "🎤 Say 'Hi Jarvis' to start chatting...";
  recognition.start();
}

function stopListening() {
  isListening = false;
  isAwake = false;
  recognition.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  statusDiv.innerText = "🛑 Chat stopped";
}

recognition.onresult = function (event) {
  const transcript = event.results[0][0].transcript.toLowerCase().trim();
  console.log("👂 Heard:", transcript);

  if (!isAwake) {
    if (transcript.includes("hi jarvis")) {
      isAwake = true;
      statusDiv.innerText = "✅ Jarvis Activated!";
      chatDiv.innerHTML += `<div><b>You:</b> ${transcript}</div>`;
      speak("Hello, I am Jarvis. How can I assist you?");
    } else {
      statusDiv.innerText = "❌ Please say 'Hi Jarvis' to begin.";
      chatDiv.innerHTML += `<div><b>Ignored:</b> ${transcript}</div>`;
    }
    setTimeout(() => recognition.start(), 2000);
    return;
  }

  // Jarvis is awake — send the voice input
  statusDiv.innerText = "🤖 Thinking...";
  chatDiv.innerHTML += `<div><b>You:</b> ${transcript}</div>`;

  fetch("/voice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: transcript }),
  })
    .then((res) => res.json())
    .then((data) => {
      const reply = data.reply;
      chatDiv.innerHTML += `<div><b>Jarvis:</b> ${reply}</div>`;
      speak(reply);
    })
    .catch((err) => {
      console.error("❌ Error:", err);
      speak("Sorry, something went wrong.");
    })
    .finally(() => {
      setTimeout(() => recognition.start(), 2000);
    });
};

recognition.onend = () => {
  if (isListening) recognition.start();
};

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}
