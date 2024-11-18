// background.js
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete") {
        const url = new URL(tab.url);
        const domain = url.hostname;

        // Request credentials from Python server
        fetch(`http://localhost:5000/get_credentials?domain=${domain}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    // Send credentials to content script to fill in the form
                    chrome.tabs.sendMessage(tabId, {
                        type: "fill_credentials",
                        username: data.account_name,
                        password: data.password
                    });
                }
            })
            .catch(error => console.error("Error fetching credentials:", error));
    }
});
