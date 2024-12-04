// This Function handles logout feature
function logoutUser() {

    // Get CSRF Token and fetch /logout method
    const csrfToken = document.getElementById('csrf-token').value;

    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Send the CSRF token in headers
        },
    })
    .then(response => {

        // Transfer to Login Page
        if (response.ok) {
            window.location.href = '/login';
        } else {
            alert('Logout failed');
        }
    })
    .catch(err => console.error(err));
}