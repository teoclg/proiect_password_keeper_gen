// Fetch existing credentials
document.getElementById('fetch-credentials').addEventListener('click', function () {
  const siteUrl = document.getElementById('site-url').value.trim();

  if (siteUrl) {
    fetch(`http://localhost:5000/get_credentials?domain=${siteUrl}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert('No credentials found for this site.');
        } else {
          document.getElementById('account-name').textContent = data.account_name || 'N/A';
          document.getElementById('password').textContent = data.password || 'N/A';
		  document.getElementById('email').textContent = data.email || 'N/A';
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

// Save new credentials
document.getElementById('save-credentials').addEventListener('click', function () {
  const siteName = document.getElementById('new-site-name').value.trim();
  const email = document.getElementById('new-email').value.trim();
  const accountName = document.getElementById('new-account-name').value.trim();
  const password = document.getElementById('new-password').value.trim();

  if (!siteName || !email || !accountName || !password) {
    alert('Please fill out all fields.');
    return;
  }

  fetch('http://localhost:5000/save_credentials', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      site_name: siteName,
      email: email,
      account_name: accountName,
      password: password,
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById('save-success').style.display = 'block';
        document.getElementById('save-error').style.display = 'none';

        // Clear input fields
        document.getElementById('new-site-name').value = '';
        document.getElementById('new-email').value = '';
        document.getElementById('new-account-name').value = '';
        document.getElementById('new-password').value = '';
      } else {
        document.getElementById('save-success').style.display = 'none';
        document.getElementById('save-error').style.display = 'block';
      }
    })
    .catch(error => {
      console.error('Error saving credentials:', error);
      document.getElementById('save-success').style.display = 'none';
      document.getElementById('save-error').style.display = 'block';
    });
});
