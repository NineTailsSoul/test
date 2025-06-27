let chatUnlocked = false;

document.addEventListener("DOMContentLoaded", function () {
    const chatItems = document.querySelectorAll(".chat-item");
    const messagesContainer = document.getElementById("chat-messages-container");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const currentChatName = document.getElementById("current-chat-name");
    const passwordInput = document.getElementById("chat-unlock-password");

    chatItems.forEach(item => {
        item.addEventListener("click", function () {
            const chatId = this.getAttribute("data-chat-id");
            const chatName = this.getAttribute("data-chat-name") || "Chat";

            // Set active UI
            document.querySelectorAll(".chat-item").forEach(c => c.classList.remove("active"));
            this.classList.add("active");
            currentChatName.textContent = `Chat with ${chatName}`;
            window.currentChatId = chatId;

            // Reset UI
            messagesContainer.innerHTML = "<p class='loading'>Loading messages...</p>";
            document.querySelector(".message-input-wrapper").style.display = "none";
            messageInput.disabled = true;
            sendButton.disabled = true;

            // Check if password already available
            const savedPass = sessionStorage.getItem("chat_unlock_pass");
            if (!savedPass) {
                passwordInput.style.display = "block";
                passwordInput.focus();

                passwordInput.onkeydown = function (e) {
                    if (e.key === "Enter") {
                        const pass = e.target.value.trim();
                        if (pass) {
                            sessionStorage.setItem("chat_unlock_pass", pass);
                            passwordInput.style.display = "none";
                            loadMessages(chatId, chatName);
                        }
                    }
                };
            } else {
                passwordInput.style.display = "none";
                loadMessages(chatId, chatName);
            }
        });
    });

    sendButton.addEventListener("click", function () {
        const content = messageInput.value.trim();
        const chatId = window.currentChatId;

        if (!chatId || !content) return;

        fetch(`/chat/send_message/${chatId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const msgDiv = document.createElement("div");
                    msgDiv.className = "message self";
                    msgDiv.textContent = `[You] ${content}`;
                    messagesContainer.appendChild(msgDiv);
                    messageInput.value = "";
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                } else {
                    alert(data.error || "Failed to send message.");
                }
            });
    });
});

function loadMessages(chatId, chatName) {
    const messagesContainer = document.getElementById("chat-messages-container");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    fetch(`/chat/get_messages/${chatId}`)
        .then(res => res.json())
        .then(messages => {
            const container = messagesContainer;
            container.innerHTML = "";

            if (Array.isArray(messages) && messages.length > 0) {
                messages.forEach(msg => {
                    const msgDiv = document.createElement("div");
                    msgDiv.className = msg.is_self ? "message self" : "message";
                    msgDiv.textContent = `[${msg.sender_username}] ${msg.content}`;
                    container.appendChild(msgDiv);
                });
            } else {
                container.innerHTML = "<p class='empty'>No messages yet. Start chatting!</p>";
            }

            container.scrollTop = container.scrollHeight;
            document.querySelector(".message-input-wrapper").style.display = "flex";
            messageInput.disabled = false;
            sendButton.disabled = false;
        })
        .catch(err => {
            console.error("Error fetching messages:", err);
            messagesContainer.innerHTML = "<p class='error'>Failed to load messages.</p>";
        });
}
