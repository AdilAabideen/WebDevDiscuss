// This file contains Javascript to Do some Clinet Side Validation for Account Page

// This function validates the Email Form 
function validateEmailForm() {
    const email = document.querySelector('input[name="email"]').value;
    const confirmEmail = document.querySelector('input[name="confirm_email"]').value;

    // Checks if they do not match
    if (email !== confirmEmail) {
        alert('Emails do not match!');
        return false;
    }
    return true;
}

// This Function validates password form
function validatePasswordForm() {
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmNewPassword = document.querySelector('input[name="confirm_new_password"]').value;
    
    // If they dont match
    if (newPassword !== confirmNewPassword) {
        alert('New passwords do not match!');
        return false;
    }
    return true;
}

// This Function validates username form
function validateUsernameForm() {
    const username = document.querySelector('input[name="username"]').value;
    const confirmUsername = document.querySelector('input[name="confirm_username"]').value;
    
    // Checks if they do not match
    if (username !== confirmUsername) {
        alert('Usernames do not match!');
        return false;
    }
    return true;
}