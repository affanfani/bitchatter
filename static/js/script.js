document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.querySelector("#chat-input");
    const sendButton = document.querySelector("#send-btn");
    const chatContainer = document.querySelector(".chat-container");
    const themeButton = document.querySelector("#theme-btn");
    const deleteButton = document.querySelector("#delete-btn");

    let userText = null;

    const updateTheme = () => {
        const themeColor = localStorage.getItem("themeColor") || "dark_mode";
        const isLightMode = themeColor === "light_mode";
        document.body.classList.toggle("light-mode", isLightMode);
        themeButton.innerText = isLightMode ? "dark_mode" : "light_mode";
        updateImages();
    };

    const updateImages = () => {
        const logoImage = document.querySelector('.default-text img');
        const botImage = document.querySelectorAll('.chat-details img[src^="static/images/BOT"]');

        if (logoImage) {
            logoImage.src = document.body.classList.contains("light-mode") ? 'static/images/Logo.png' : 'static/images/Logo Darkmode.png';
        }
        botImage.forEach(img => {
            img.src = document.body.classList.contains("light-mode") ? 'static/images/BOT.png' : 'static/images/BOT Darkmode.png';
        });
    };

    const loadDataFromLocalstorage = () => {
        const defaultText = `
            <center><div class="default-text">
                <h1>BIT Chatter</h1>
                <img src="${document.body.classList.contains("light-mode") ? 'static/images/Logo.png' : 'static/images/Logo Darkmode.png'}"
                    alt="" style="width: 200px; height: 200px;">
                <p>Start a conversation and explore IBIT.<br> Your conversation will be displayed here.</p>
            </div></center>`;
        chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
        updateImages();
    };

    const createChatElement = (content, className) => {
        const chatDiv = document.createElement("div");
        chatDiv.classList.add("chat", className);
        chatDiv.innerHTML = content;
        return chatDiv;
    };

    const getChatResponse = async (incomingChatDiv) => {
        const API_URL = "/get_response";
        const pElement = document.createElement("p");

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: userText })
        };

        try {
            const response = await fetch(API_URL, requestOptions);
            const responseData = await response.json();
            pElement.textContent = responseData.response;
        } catch (error) {
            pElement.classList.add("error");
            pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
        }

        incomingChatDiv.querySelector(".typing-animation").remove();
        incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
        localStorage.setItem("all-chats", chatContainer.innerHTML);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    };

    const showTypingAnimation = () => {
        const html = `<div class="chat-content">
                        <div class="chat-details">
                            <img src="static/images/BOT.png" alt="chatbot-img">
                            <div class="typing-animation">
                                <div class="typing-dot" style="--delay: 0.2s"></div>
                                <div class="typing-dot" style="--delay: 0.3s"></div>
                                <div class="typing-dot" style="--delay: 0.4s"></div>
                            </div>
                        </div>
                        <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                    </div>`;
        const incomingChatDiv = createChatElement(html, "incoming");
        chatContainer.appendChild(incomingChatDiv);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
        getChatResponse(incomingChatDiv);
    };

    const handleOutgoingChat = () => {
        userText = chatInput.value.trim();
        if (!userText) return;

        chatInput.value = "";

        const html = `<div class="chat-content">
                        <div class="chat-details">
                            <img src="static/images/user.png" alt="user-img">
                            <p>${userText}</p>
                        </div>
                    </div>`;
        const outgoingChatDiv = createChatElement(html, "outgoing");
        chatContainer.querySelector(".default-text")?.remove();
        chatContainer.appendChild(outgoingChatDiv);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
        setTimeout(showTypingAnimation, 500);
    };

    deleteButton.addEventListener("click", () => {
        if (confirm("Are you sure you want to delete all the chats?")) {
            localStorage.removeItem("all-chats");
            loadDataFromLocalstorage();
        }
    });

    themeButton.addEventListener("click", () => {
        const currentTheme = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
        localStorage.setItem("themeColor", currentTheme);
        updateTheme();
    });

    chatInput.addEventListener("input", () => {
        chatInput.style.height = "auto";
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleOutgoingChat();
        }
    });

    sendButton.addEventListener("click", handleOutgoingChat);
    loadDataFromLocalstorage();
});
