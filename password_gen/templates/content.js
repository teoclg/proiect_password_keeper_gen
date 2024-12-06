// content.js
function fillPassword(username, password) {
    const usernameField = document.querySelector("input[type='text'], input[type='email']");
    const passwordField = document.querySelector("input[type='password']");

    if (usernameField && passwordField) {
        usernameField.value = username;
        passwordField.value = password;
    }
}

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "fill_credentials") {
        fillPassword(message.username, message.password);
    }
});

