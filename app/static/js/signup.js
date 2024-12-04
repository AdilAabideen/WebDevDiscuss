
// This function Validates the Signup Data Client Side, If fail reset form
function validateSignupForm(event) {

    // Get Data Elements
    const firstname = document.querySelector('input[name="firstname"]').value;
    const lastname = document.querySelector('input[name="lastname"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;

    // Regex Function to check if it includes the Characters
    const nameRegex = /^[a-zA-Z]+$/;

    // Check Firstname if it includes special chars or numbers
    if (!nameRegex.test(firstname)) {
        alert("First Name should not contain numbers or special characters.");
        event.preventDefault();
        return false;
    }

    // Check lastname if it includes special chars or numbers
    if (!nameRegex.test(lastname)) {
        alert("Last Name should not contain numbers or special characters.");
        event.preventDefault();
        return false;
    }

    // Checl if Email includes a @
    if (!email.includes('@')) {
        alert("Email must contain an '@' symbol.");
        event.preventDefault();
        return false;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        alert("Password and Confirm Password must match.");
        event.preventDefault();
        return false;
    }

    return true;
}