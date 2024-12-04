// Jquery, AJAX Fetch Functions
$(document).ready(function () {

    // Handle follow and unfollow functionality
    $(document).on('click', '.follow-btn-submit', function (e) {
        e.preventDefault();

        const button = $(this);
        const userId = button.data('user-id');

        // Make AJAX request
        $.ajax({
            url: `/follow/${userId}`,
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') // CSRF protection
            },
            success: function (response) {
                if (response.success) {

                    // Update button text and class dynamically
                    
                    button.text('Unfollow');

                    button.addClass('btn-unfollow');
                    
                    
                } else {
                    button.text('Follow');
                    button.removeClass('btn-unfollow');
                   
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    });


    // Handle like button functionality
    $('.like-button').each(function () {

        // Data Elements
        const button = $(this);
        const postId = button.data('post-id');
        const likeIcon = $(`#like-icon-${postId}`);
        const likeCountElement = $(`#like-count-${postId}`);
        let liked = button.data('liked') === true;

        button.on('click', function (e) {
            e.preventDefault();

            // Make Ajax Request
            $.ajax({
                url: `/like/${postId}`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'), // CSRF protection
                },
                success: function (data) {

                    // If Success Toggle State and Update Data Dynamically
                    if (data.success) {
                        
                        liked = !liked;
                        button.data('liked', liked);
                        likeCountElement.text(data.likes);

                        // Update heart icon styling to show if liked
                        if (liked) {
                            likeIcon.removeClass('far').addClass('fas text-danger'); // Red filled heart
                        } else {
                            likeIcon.removeClass('fas text-danger').addClass('far'); // Outlined heart
                        }
                    } else {
                        alert(data.error || 'Failed to like the post.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                    alert('Failed to like the post. Please try again.');
                },
            });
        });
    });

    // Handle comment adding functionality
    $('.subm-btn').each(function () {
        const button = $(this);

        button.on('click', function (e) {
            e.preventDefault();
            console.log('Comment button clicked.'); // Debugging

            const commentForm = button.closest('.view-post-search-bar');
            const commentInput = commentForm.find('input');
            const postId = commentForm.data('post-id');
            const commentText = commentInput.val().trim();

            if (!commentText) {
                alert('Comment cannot be empty.');
                return;
            }

            // Make AJAX Request
            $.ajax({
                url: `/add_comment/${postId}`,
                type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'), // CSRF protection
                },
                data: JSON.stringify({ body: commentText }),
                success: function (data) {

                    // If Success add New Comment and Update count and Styles Dynamically
                    if (data.success) {
                        commentInput.val(''); 
                        const commentsSection = $('.view-post-comments-section');

                        const newComment = $(`<p class="mb-2"><strong>${data.comment.author}</strong>: ${data.comment.body}</p>`);
                        commentsSection.prepend(newComment);

                        const commentCount = $(`#comment-count-${postId}`);
                        if (commentCount.length) {
                            commentCount.text(data.comment_count);
                        }
                    } else {
                        console.error('Failed to submit comment:', data.error);
                        alert(data.error || 'Failed to submit comment.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error submitting comment:', error);
                    alert('An error occurred while submitting the comment.');
                },
            });
        });
    });

    // Handle share functionality
    $('.share-button').each(function () {
        const button = $(this);
        const postId = button.data('post-id');
        const shareCountElement = $(`#share-count-${postId}`);
        let shared = button.data('shared') === true;

        button.on('click', async function (e) {
            e.preventDefault();

            if (shared) {
                alert('You have already shared this post.');
                return;
            }

            try {
                // Copy the URL to the clipboard
                const postUrl = `${window.location.origin}/post/${postId}`;
                await navigator.clipboard.writeText(postUrl);

                // Make AJAX Request
                $.ajax({
                    url: `/share/${postId}`,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'), // CSRF protection
                    },
                    success: function (data) {

                        // If Success update Count Dynamically
                        if (data.success) {
                            shared = true;
                            button.data('shared', true);
                            shareCountElement.text(data.shares);
                            alert('Link copied to clipboard and share count incremented!');
                        } else {
                            alert(data.error || 'Failed to share the post.');
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error('Error:', error);
                        alert('Failed to share the post. Please try again.');
                    },
                });
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to copy the link to clipboard.');
            }
        });
    });
});

