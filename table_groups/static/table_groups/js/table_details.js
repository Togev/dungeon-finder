let lastMessageId = 0;

const messageListContainer = document.getElementById('message-list-container');
const ajaxMessagesUrl = messageListContainer.dataset.ajaxTableMessagesUrl;

const messageList = messageListContainer.querySelector('.message-list');
const messageSendForm = document.getElementById('message-send-form');

document.querySelectorAll('.message-block-content').forEach(function(el) {
    const mid = parseInt(el.getAttribute('data-message-id'));
    if (mid > lastMessageId) lastMessageId = mid;
});

function attachDeleteListeners() {
    document.querySelectorAll('.inline-message-delete-form').forEach(function(form) {
        if (form.dataset.listenerAttached === "true") return;
        form.dataset.listenerAttached = "true";

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const actionUrl = form.action;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(actionUrl, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.ok) {
                    const li = form.closest('.message-block-content');
                    if (li) li.remove();
                } else {
                    alert('Failed to delete message.');
                    console.error('Failed to delete message:', response);
                }
            })
            .catch(error => {
                alert('Error deleting message.');
                console.error('Error deleting message:', error);
            });
        });
    });
}

function pollMessages() {
    fetch(ajaxMessagesUrl + "?after=" + lastMessageId)
        .then(response => response.json())
        .then(data => {
            if (data.messages_html && data.messages_html.trim()) {
                const emptyMsg = messageList.querySelector('.empty-messages-list');
                if (emptyMsg) {
                    emptyMsg.remove();
                }

                let tempDiv = document.createElement('div');
                tempDiv.innerHTML = data.messages_html;
                tempDiv.querySelectorAll('.message-block-content').forEach(function(newEl) {
                    messageList.appendChild(newEl);
                    const mid = parseInt(newEl.getAttribute('data-message-id'));
                    if (mid > lastMessageId) lastMessageId = mid;
                });
                attachDeleteListeners();
            }
        })
        .catch(error => console.error('Error polling messages:', error));
}
setInterval(pollMessages, 7000);

document.addEventListener('DOMContentLoaded', function() {
    attachDeleteListeners();

    if (messageSendForm) {
        messageSendForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(messageSendForm);

            fetch(messageSendForm.action, {
                method: 'POST',
                body: formData,
                credentials: 'same-origin',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    messageSendForm.reset();
                    pollMessages();
                } else {
                    alert('Error sending message.');
                    console.error('Error submitting message:', response);
                }
            })
            .catch(error => {
                alert('Error submitting message.');
                console.error('Error submitting message:', error);
            });
        });

        const textarea = messageSendForm.querySelector('#id_content');
        if (textarea) {
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    messageSendForm.requestSubmit();
                }
            });
        }
    }
});