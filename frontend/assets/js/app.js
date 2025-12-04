document.addEventListener('DOMContentLoaded', () => {
    // Navigation Logic
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view-section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = item.getAttribute('data-tab');

            // Update Nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update View
            views.forEach(view => {
                view.style.display = 'none';
                view.classList.remove('active');
            });

            const targetView = document.getElementById(`${targetId}-view`);
            if (targetView) {
                targetView.style.display = 'block';
                // Small delay for fade-in effect if we added one
                setTimeout(() => targetView.classList.add('active'), 10);
            }
        });
    });

    // Simulator Logic
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-chat');

    function addMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', role);
        msgDiv.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function handleSend() {
        const text = userInput.value.trim();
        if (!text) return;

        // Add User Message
        addMessage('user', text);
        userInput.value = '';

        // Simulate API Call (Replace with real API later)
        // For now, we mock the response to show UI functionality
        addMessage('assistant', 'Thinking...');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    history: [] // In a real app, we'd maintain history here
                })
            });

            // Remove "Thinking..."
            if (chatMessages.lastElementChild.textContent === "Thinking...") {
                chatMessages.lastElementChild.remove();
            }

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            addMessage('assistant', data.response);

        } catch (error) {
            console.error(error);
            // Remove "Thinking..." if it exists
            if (chatMessages.lastElementChild.textContent === "Thinking...") {
                chatMessages.lastElementChild.remove();
            }
            addMessage('system', 'Error connecting to agent. Is the server running?');
        }
    }

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    clearBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '<div class="message system"><p>Simulation started. Type a message to interact with Alex.</p></div>';
    });
});
