// AJAX for following and Unfollowing
$(document).on('click', '.unfollow', function (e) {
    e.preventDefault();

    const button = $(this);
    const userId = button.data('user-id');

    // Make AJAX request
    $.ajax({
        url: `/unfollow/${userId}`,
        type: 'POST',
        headers: {
            'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') // CSRF protection
        },
        success: function (response) {
            // Update button text and class dynamically if Success
            if (response.success) {
                
                button.text('Follow');
                button.removeClass('btn-danger unfollow-btn-submit');
                button.addClass('btn-success follow-btn-submit');

                alert(response.message || 'Successfully unfollowed!');
            } else {
                alert(response.message || 'Failed to unfollow. Please try again.');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
});