function fillPassword(username, password) {
    const usernameField = document.querySelector("input[type='text'], input[type='email']");
    const passwordField = document.querySelector("input[type='password']");

    if (usernameField && passwordField) {
        // Fill the username field only if it is empty
        usernameField.addEventListener('click', () => {
            if (!usernameField.value) {
                usernameField.value = username;
            }
        });

        // Fill the password field only if it is empty
        passwordField.addEventListener('click', () => {
            if (!passwordField.value) {
                passwordField.value = password;
            }
        });

        // Ensure the fields don't lose the value once filled
        usernameField.addEventListener('focusout', () => {
            if (usernameField.value && usernameField.value !== username) {
                usernameField.value = username;
            }
        });

        passwordField.addEventListener('focusout', () => {
            if (passwordField.value && passwordField.value !== password) {
                passwordField.value = password;
            }
        });
    }
}

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "fill_credentials") {
        fillPassword(message.username, message.password);
    }
});
