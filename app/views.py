"""This file Contains the Views for each page and API calls to make changes to the Data"""

from app import app, db
from flask import render_template, flash, redirect, url_for, jsonify, request, session
from app.forms import AddPostForm, UpdateNameForm, UpdateEmailForm, UpdatePasswordForm, UpdateUsernameForm, LoginForm, SignupForm, LoginForm
from app.models import Post, User, Comment
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from sqlalchemy.orm import joinedload

@app.route('/')
def index():
    """This Function Returns Homepage"""

    return render_template('home.html')

# Function to ensure all routes are protected
def protected_route(func):
    """This Function Make sure Pages are protected, only for Logged in Users"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to log in to access this page.', 'warning')

            # If they are not logged in return to /login page
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# Main page app route
@app.route('/main')
@protected_route
def main():
    """This Function Returns all Posts and if they are liked, and also all posts based on a recommendation algorithm"""
    # Get Current User
    user = current_user

    # Get the search query, default to an empty string if empty
    query = request.args.get('q', '').strip()

    # Filter posts based on the search query or load all posts if search query is empty
    if query:
        posts = Post.query.options(joinedload(Post.user)).filter(
            (Post.title.ilike(f'%{query}%')) |
            (Post.body.ilike(f'%{query}%')) |
            (Post.tags.ilike(f'%{query}%'))
        ).all()
    else:
        posts = Post.query.options(joinedload(Post.user)).all()

    # Add a liked property to each post for the template if they are liked by the user
    for post in posts:
        post.liked = user in post.liked_by.all()

    # Recommendation Algo 
    # IDs of friends
    friends_ids = [friend.id for friend in user.followed]

    # Posts from Friends
    friends_posts = Post.query.filter(Post.user_id.in_(friends_ids)).options(joinedload(Post.user)).all()

    # Posts not by friends
    other_posts = Post.query.filter(~Post.user_id.in_(friends_ids)).options(joinedload(Post.user)).all()

    # Define weights for ranking for the recommendation algorithm
    like_weight = 3
    comment_weight = 2
    share_weight = 1

    # Function that Rank the posts by a weighted score
    def rank_post(post):
        return (
            (post.likes or 0) * like_weight +
            (post.comments_count or 0) * comment_weight +
            (post.shares or 0) * share_weight
        )

    # Sort posts by rank
    ranked_other_posts = sorted(other_posts, key=rank_post, reverse=True)

    # Combine friends posts with top-ranked other posts
    recommended_posts = friends_posts + ranked_other_posts[:max(0, 5 - len(friends_posts))]

    # Add a Liked part to show if it is liked
    for post in recommended_posts:
        post.liked = user in post.liked_by.all()

    return render_template('main.html', posts=posts, query=query, recommended_posts=recommended_posts)


@app.route('/addpost', methods=['GET', 'POST'])
@protected_route
def addpost():
    """This Function Takes in Data and Creates a New Post"""
    # Create New Form
    form = AddPostForm()

    if form.validate_on_submit():

        # Create New Post
        new_post = Post(
            title=form.title.data,
            tags=form.tags.data,
            body=form.description.data,
            code_snippet=form.code_snippet.data,
            user_id=current_user.id  # Replace with the logged-in user ID
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f"New post '{form.title.data}' created successfully!", 'success')
        return redirect(url_for('main'))
    else:
        # If there are errors
        if form.errors:
            print("Form Errors:", form.errors)

    return render_template('addpost.html', form=form, title="Add New Post")



@app.route('/like/<int:post_id>', methods=['POST'])
@protected_route
def like_post(post_id):
    """This Function Takes a Post id and adds a like for a User in it"""

    # Get Post and Current User
    user = current_user
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Check if the user has already liked the post
    if post in user.liked_posts:
        
        # If they have Unlike the Post
        user.liked_posts.remove(post)
        post.likes -= 1
        db.session.commit()

        # Return Json Message
        return jsonify({'success': True, 'likes': post.likes, 'liked': False})

    # Else Like the post, increment like counter
    user.liked_posts.append(post)
    post.likes += 1
    db.session.commit()

    # Return Json Message
    return jsonify({'success': True, 'likes': post.likes, 'liked': True})

@app.route('/main/<int:id>', methods=['GET'])
@protected_route
def view_post(id):
    """This Function returns the full data about a singular post, based on post id"""

    # Retrieve the post based on its ID, Automatically return 404 if not found
    post = Post.query.get_or_404(id)

    # Return the Post and if it is liked
    user = current_user
    post.liked = user in post.liked_by.all()

    return render_template('view_post.html', post=post)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
@protected_route
def add_comment(post_id):
    """This Function Adds a comment to a specific post"""
    
    # Get current User
    user = current_user
    user_id = user.id

    # Get the Post
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    # If data is not recieved for the comment
    if not data or not data.get('body'):
        return jsonify({'error': 'Comment body cannot be empty'}), 400

    # Create new Comment and increment num of comments
    comment = Comment(body=data['body'], user_id=user_id, post_id=post.id)
    db.session.add(comment)
    post.comments_count = (post.comments_count or 0) + 1  # Fallback to 0 if None
    db.session.commit()

    # Return json message, to signal increase in comment counts and add comment to UI
    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'body': comment.body,
            'author': comment.author.username,  # Assuming `username` exists on the `User` model
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        },
        'comment_count' : post.comments_count
    })

@app.route('/share/<int:post_id>', methods=['POST'])
@protected_route
def share_post(post_id):
    """
    This Function Increments the shares count for a post.
    """
    

    # Retrieve the post by its ID
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Increment the shares count
    post.shares = (post.shares or 0) + 1
    db.session.commit()

    # Respond with JSON success and the updated shares count
    return jsonify({'success': True, 'shares': post.shares})



@app.route('/account', methods=['GET', 'POST'])
@protected_route
def account():
    """This Function Returns forms for the account page."""

    # Return User and the Forms to display data and forms
    user = current_user 
    name_form = UpdateNameForm()
    email_form = UpdateEmailForm()
    password_form = UpdatePasswordForm()
    username_form = UpdateUsernameForm()

    return render_template(
        'account.html', 
        user=user, 
        name_form=name_form, 
        email_form=email_form, 
        password_form=password_form, 
        username_form=username_form
    )


@app.route('/update_name', methods=['POST'])
@protected_route
def update_name():
    """This Function Updates the Users Name """
    form = UpdateNameForm()
    user = current_user

    # Get Firstname nad Lastname and Updated it if server side validation is successful
    if form.validate_on_submit():
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        db.session.commit()
        flash('Name updated successfully!', 'success')
    else:
        flash('Error updating name', 'danger')
    return redirect(url_for('account'))


@app.route('/update_email', methods=['POST'])
@protected_route
def update_email():
    """This Function updates the Email of the user"""

    form = UpdateEmailForm()
    user = current_user

    # Set email if server side validation is successful
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.commit()
        flash('Email updated successfully!', 'success')
    else:
        flash('Error updating email', 'danger')
    return redirect(url_for('account'))


@app.route('/update_password', methods=['POST'])
@protected_route
def update_password():
    """This Function updates users password"""
    form = UpdatePasswordForm()
    user = current_user

    # Change password if server side validation is successful
    if form.validate_on_submit():
        # Check if old password is correct, then set new password
        if user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        else:
            flash('Old password is incorrect', 'danger')
    else:
        flash('Error updating password', 'danger')
    return redirect(url_for('account'))


@app.route('/update_username', methods=['POST'])
@protected_route
def update_username():
    """This Function updates the Users Username """

    form = UpdateUsernameForm()
    user = current_user

    # Change username if server side validation is successful 
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        flash('Username updated successfully!', 'success')
    else:
        flash('Error updating username', 'danger')
    return redirect(url_for('account'))


@app.route('/signup', methods=['GET', 'POST'])

def signup():
    """This Function sings and creates a new user"""

    # Redirect to main page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    # IF PASS Server Side Validation
    form = SignupForm()
    if form.validate_on_submit():

        # Checking if the email already exists in table, if so flash an error
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash('Email already exists. Please use a different email.', 'danger')
            print("Email already exists")
            return render_template('signup.html', form=form)

        # Check if the username already exists, if so flash an error
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        if existing_user_username:
            flash('Username already exists. Please choose a different username.', 'danger')
            print("Username already exists")
            return render_template('signup.html', form=form)

        # Check if both passwords provided match, if not flash an error
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'danger')
            print("Passwords do not match")  # Debug log
            return render_template('signup.html', form=form)

        # Create and save the user
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            username=form.username.data,
        )
        user.set_password(form.password.data)  # Assuming set_password hashes the password
        db.session.add(user)
        db.session.commit()

        # Log the user in after signup and flash success message and redirect to main page
        login_user(user)
        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('main'))
    else:
        # Debug Errors
        print("Form validation failed")
        print(form.errors)

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This Function Logs the User in"""

    # Redirect to main page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginForm()  
    # If login data is server side validated
    if form.validate_on_submit(): 

        # Check if the user exists
        user = User.query.filter_by(email=form.email.data).first()

        # If Exists, check the passwords with hash
        if user and user.check_password(form.password.data):

             # If match log in user and redirect
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:

            # Flash error to signify invalid data
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """This Function Logs the user out"""

    # Log out User
    logout_user()
    flash('You have been logged out.', 'success')
    return '', 204 

@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    """This Function Follows the User"""

    # Get the User we need to follow
    user_to_follow = User.query.get_or_404(user_id)
    
    # Check if the current user is already following the target user
    if current_user.is_following(user_to_follow):

        # If so Unfollow the User and return Json Message
        current_user.unfollow(user_to_follow)
        return jsonify({'success': False, 'message': f'You have unfollowed {user_to_follow.username}', 'followed': False})
    
    # Else Follow the User and return JSON Message
    current_user.follow(user_to_follow)
    return jsonify({'success': True, 'message': f'You are now following {user_to_follow.username}', 'followed': True})


@app.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    """This Function Unfollows the User"""

    # Get the user to unfollow
    user_to_unfollow = User.query.get_or_404(user_id)

    # Check if the current user is already not following the user, if so return JSON message
    if not current_user.is_following(user_to_unfollow):
        return jsonify({'success': False, 'message': 'You are not following this user.'}), 400

    # Remove the following relationship
    current_user.unfollow(user_to_unfollow)
    db.session.commit()

    return jsonify({'success': True, 'message': f'You have unfollowed {user_to_unfollow.username}.'})

@app.route('/user_post', methods=['GET'])
@login_required
def user_dashboard():
    """This Function returns Data for User Dashboard"""

    # Get the current user
    user = current_user

    # Get the user's posts
    user_posts = user.posts

    # Get the posts liked by the user
    liked_posts = user.liked_posts.all()

    # Get the people the user follows
    followed_users = user.followed.all()

    # Return the Data
    return render_template(
        'user_post.html',
        user=user,
        user_posts=user_posts,
        liked_posts=liked_posts,
    )
      
@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    """This Function Allows User to Edit Post"""

    # Get Post By ID
    post = Post.query.get_or_404(post_id)

    # Ensure the current user is the author of the post
    if post.user_id != current_user.id:
        flash("You do not have permission to edit this post.", "danger")
        return redirect(url_for("main"))

    form = AddPostForm()

    # Handle POST Form, Pre Add Data
    if form.validate_on_submit():
        post.title = form.title.data
        post.tags = form.tags.data
        post.body = form.description.data
        post.code_snippet = form.code_snippet.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("main"))

    # Pre-fill the form with the post's existing data for GET request
    form.title.data = post.title
    form.tags.data = post.tags
    form.description.data = post.body
    form.code_snippet.data = post.code_snippet

    return render_template("edit_post.html", form=form, post=post)