document.getElementById('fetch-credentials').addEventListener('click', function () {
  // Get the website URL entered by the user
  const siteUrl = document.getElementById('site-url').value.trim();
  
  if (siteUrl) {
    // Fetch the credentials from the backend (Flask server)
    fetch(`http://localhost:5000/get_credentials?domain=${siteUrl}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert('No credentials found for this site.');
        } else {
          // Populate the fields with the credentials
          document.getElementById('account-name').textContent = data.account_name || 'N/A';
          document.getElementById('password').textContent = data.password || 'N/A';
        }
      })
      .catch(error => {
        console.error("Error fetching credentials:", error);
        alert('Error fetching credentials.');
      });
  } else {
    alert('Please enter a valid site URL.');
  }
});
