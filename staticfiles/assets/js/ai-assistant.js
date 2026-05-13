(function () {
  function getCookie(name) {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));
    return cookieValue ? decodeURIComponent(cookieValue.split("=")[1]) : "";
  }

  function appendMessage(container, text, className) {
    const msg = document.createElement("div");
    msg.className = "ai-msg " + className;
    msg.textContent = text;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
  }

  function canUseSpeechRecognition() {
    return "SpeechRecognition" in window || "webkitSpeechRecognition" in window;
  }

  function createSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return null;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;
    return recognition;
  }

  function speakText(text) {
    if (!("speechSynthesis" in window) || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
    window.speechSynthesis.speak(utterance);
  }

  document.addEventListener("DOMContentLoaded", function () {
    const mainBtn = document.getElementById("aiMainBtn");
    const menu = document.getElementById("aiMenu");
    const chatBtn = document.getElementById("aiChatBtn");
    const voiceBtn = document.getElementById("aiVoiceBtn");
    const playBtn = document.getElementById("aiPlayBtn");
    const panel = document.getElementById("aiChatPanel");
    const closeChatBtn = document.getElementById("aiCloseChat");
    const form = document.getElementById("aiChatForm");
    const input = document.getElementById("aiChatInput");
    const body = document.getElementById("aiChatBody");
    const sendBtn = document.getElementById("aiSendBtn");
    const recognition = createSpeechRecognition();
    let isListening = false;

    if (!mainBtn || !menu || !chatBtn || !panel || !form || !input || !body) {
      return;
    }

    async function sendMessage(text, fromVoice) {
      appendMessage(body, text, "ai-msg-user");
      input.value = "";
      sendBtn.disabled = true;

      try {
        const res = await fetch("/api/ai/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ message: text }),
        });

        const data = await res.json();
        if (res.ok && data.ok) {
          appendMessage(body, data.reply, "ai-msg-bot");
          if (fromVoice) {
            speakText(data.reply);
          }
        } else {
          appendMessage(
            body,
            data.error || "Sorry, I could not process that right now.",
            "ai-msg-bot"
          );
        }
      } catch (err) {
        appendMessage(body, "Network issue. Please try again.", "ai-msg-bot");
      } finally {
        sendBtn.disabled = false;
        input.focus();
      }
    }

    mainBtn.addEventListener("click", function () {
      menu.classList.toggle("active");
    });

    chatBtn.addEventListener("click", function () {
      panel.classList.toggle("open");
      if (panel.classList.contains("open")) {
        input.focus();
      }
    });

    if (closeChatBtn) {
      closeChatBtn.addEventListener("click", function () {
        panel.classList.remove("open");
      });
    }

    if (voiceBtn) {
      voiceBtn.addEventListener("click", function () {
        panel.classList.add("open");
        if (!recognition || !canUseSpeechRecognition()) {
          appendMessage(
            body,
            "Voice input is not supported in this browser. Please type your message.",
            "ai-msg-bot"
          );
          return;
        }

        if (isListening) {
          recognition.stop();
          return;
        }

        try {
          recognition.start();
        } catch (e) {
          appendMessage(body, "Microphone is busy. Please try again.", "ai-msg-bot");
        }
      });
    }

    if (recognition && voiceBtn) {
      recognition.onstart = function () {
        isListening = true;
        voiceBtn.classList.add("listening");
        appendMessage(body, "Listening... Speak now.", "ai-msg-bot");
      };

      recognition.onresult = function (event) {
        const transcript = (event.results?.[0]?.[0]?.transcript || "").trim();
        if (transcript) {
          sendMessage(transcript, true);
        } else {
          appendMessage(body, "I could not hear clearly. Please try again.", "ai-msg-bot");
        }
      };

      recognition.onerror = function () {
        appendMessage(body, "Voice input error. Please allow microphone access.", "ai-msg-bot");
      };

      recognition.onend = function () {
        isListening = false;
        voiceBtn.classList.remove("listening");
      };
    }

    if (playBtn) {
      playBtn.addEventListener("click", function () {
        appendMessage(
          body,
          "Tip: Ask about SG.Automix Tech services, courses, or certification.",
          "ai-msg-bot"
        );
        panel.classList.add("open");
      });
    }

    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      sendMessage(text, false);
    });
  });
})();
