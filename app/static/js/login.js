
// Function to Validate the Login, Checks if email includes a @
function validateLoginForm(event) {
            
    const email = document.querySelector('input[name="email"]').value;

    // If not then return False
    if (!email.includes('@')) {
        alert("Email must contain an '@' symbol.");
        event.preventDefault();
        return false;
    }

    

    return true;
}