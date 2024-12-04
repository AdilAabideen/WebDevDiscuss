// javascript for client side validation when adding a Post

document.querySelector('form').addEventListener('submit', function(event) {

    // Get Elements
    const title = document.getElementById('title').value.trim();
    const tags = document.getElementById('tags').value.trim();
    const description = document.getElementById('description').value.trim();
    const codeSnippet = document.getElementById('codeSnippet').value.trim();
    let isValid = true;

    // Checks if title contains letters
    if (!/[a-zA-Z]/.test(title)) {
        alert('Title must contain letters.');
        isValid = false;
    }

    // Tags cannot be greater than length 200
    if (tags.length > 200) {
        alert('Tags must not exceed 200 characters.');
        isValid = false;
    }

    // Description has to include letters
    if (!/[a-zA-Z]/.test(description)) {
        alert('Description must contain letters.');
        isValid = false;
    }

    // Code snippet cannot be greater than 1000 characters in length
    if (codeSnippet.length > 1000) {
        alert('Code snippet must not exceed 1000 characters.');
        isValid = false;
    }

    // If it fails client side validation then Prevent form submission
    if (!isValid) {
        event.preventDefault(); 
    }
});