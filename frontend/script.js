const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const ratingBox = document.getElementById("rating-box");

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    addMessage(message, "user");
    messageInput.value = "";

    fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
    })
    .then((res) => res.json())
    .then((data) => {
        addMessage(data.reply, "bot");

        // Show rating stars if bot asks for rating
        if (data.reply.includes("Please rate your chat")) {
            ratingBox.style.display = "block";
        }
    });
}

function addMessage(msg, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = msg;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle star rating clicks
ratingBox.querySelectorAll(".star").forEach((star) => {
    star.addEventListener("click", () => {
        const rating = star.dataset.value;
        // Highlight stars
        ratingBox.querySelectorAll(".star").forEach((s) => {
            s.classList.toggle("selected", s.dataset.value <= rating);
        });

        addMessage(`You rated: ${rating} star(s)`, "user");
        ratingBox.style.display = "none";

        // Optionally send rating to backend
        fetch("http://127.0.0.1:8000/rating", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ rating: parseInt(rating) }),
        });
    });
});
