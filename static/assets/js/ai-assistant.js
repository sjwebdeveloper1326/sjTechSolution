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

    if (!mainBtn || !menu || !chatBtn || !panel || !form || !input || !body) {
      return;
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
        appendMessage(body, "Voice mode will be available soon.", "ai-msg-bot");
        panel.classList.add("open");
      });
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
    });
  });
})();
