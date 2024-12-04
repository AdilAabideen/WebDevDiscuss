// JavaScript for Main Page
document.addEventListener('DOMContentLoaded', () => {

    // AJAX Logic for Like functionality
    document.querySelectorAll('.like-button').forEach(button => {
        const likeIcon = button.querySelector('.like-icon');

        // Check if the button is already liked, if so remove classlists at page load
        const isLiked = button.getAttribute('data-liked') === 'true';
        if (isLiked) {
            likeIcon.classList.remove('far');
            likeIcon.classList.add('fas', 'text-danger');
        }

        
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default behavior

            const postId = this.getAttribute('data-post-id');
            const likeCountElement = document.getElementById(`like-count-${postId}`);

            // Make Ajax Request
            $.ajax({
                url: `/like/${postId}`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
                },
                success: function (data) {

                    // If Success Update like count and Add classes to show on UI a Change
                    if (data.success) {
                        likeCountElement.textContent = data.likes;
                        if (data.liked) {
                            likeIcon.classList.remove('far');
                            likeIcon.classList.add('fas', 'text-danger');
                            button.setAttribute('data-liked', 'true');
                        } else {
                            likeIcon.classList.remove('fas', 'text-danger');
                            likeIcon.classList.add('far');
                            button.setAttribute('data-liked', 'false');
                        }
                    } else {
                        alert(data.error || 'An error occurred.');
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        });
    });

    // AJAX logic for Live Search functionality
    $('.form-control').on('input', function () {
        const query = $(this).val().trim();

        // Only perform a search after 3 characters typed in
        if (query.length > 2) {

            // AJAX Request
            $.ajax({
                url: `/main?q=${encodeURIComponent(query)}`,
                type: 'GET',
                success: function (response) {

                    // Parse the returned HTML and replace the content with new content posts
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(response, 'text/html');
                    const newContent = doc.querySelector('.row.p-4.py-0').innerHTML;
                    $('.row.p-4.py-0').html(newContent);
                },
                error: function (error) {
                    console.error('Error fetching search results:', error);
                }
            });
        }
    });
});