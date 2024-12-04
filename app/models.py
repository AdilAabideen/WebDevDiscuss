"""This file Contains the Database models for User, Posts, Comments and Association tables for the Many to Many Relationships"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Association Table for Likes
likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# Association Table for Friends
friends = db.Table(
    'friends',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Model Schema for the User Data Base
class User(db.Model, UserMixin):
    """This Class defines the User Model"""

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    liked_posts = db.relationship(
        'Post', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'), lazy='dynamic'
    )

    # Friends. People that follow or they follow
    followed = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.follower_id == id),
        secondaryjoin=(friends.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        """This Function returns a String representation"""

        return f"<User {self.username}>"

    # Method to Follow another Users
    def follow(self, user):
        """Follow another user."""
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    # Method to Unfollow another User
    def unfollow(self, user):
        """Unfollow another user."""
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    # Method to check if they are following that User
    def is_following(self, user):
        """Check if the user is following another user."""
        return self.followed.filter(friends.c.followed_id == user.id).count() > 0

    # Method to check if user is followed by a person
    def is_followed_by(self, user):
        """Check if the user is followed by another user."""
        return self.followers.filter(friends.c.follower_id == user.id).count() > 0

    # Method to Like a Post
    def like_post(self, post):
        """Like a post if not already liked."""
        if not self.has_liked_post(post):
            self.liked_posts.append(post)
            return True
        return False

    # Method to Unlike a Post
    def unlike_post(self, post):
        """Unlike a post if already liked."""
        if self.has_liked_post(post):
            self.liked_posts.remove(post)
            return True
        return False

    # Method to set a Password, Making sure it is hashed
    def set_password(self, password):
        """Hash the password and store it in the database."""
        self.password_hash = generate_password_hash(password)

    # Method to Check the password with hashed password
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    # Checks if user has liked the post
    def has_liked_post(self, post):
        """Check if the user has already liked the post."""
        return self.liked_posts.filter(likes.c.post_id == post.id).count() > 0


# Model Schema for Post table
class Post(db.Model):
    """This Class defines the Post Model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    code_snippet = db.Column(db.Text, nullable=True)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade="all, delete-orphan")
    user = db.relationship('User', backref='posts')
    
    
    # Constructor to generate Slug for routing
    def __init__(self, **kwargs):
        """This Constructor sets up Slug field"""
        super().__init__(**kwargs)
         # Generate slug if not explicitly provided
        if not self.slug:
            self.slug = self.generate_slug()

    # Method to generate slug depending on title
    def generate_slug(self):
        """Generate slug based on the title."""
        return self.title.replace(" ", "-").lower()

    def __repr__(self):
        return f"<Post {self.title}>"

    # Method to add a comment to the post
    def add_comment(self, comment):
        """Add a comment to the post and increment the comments_count."""
        self.comments.append(comment)
        self.comments_count += 1
        db.session.commit()

    # Method to Remove a Comment from the Post
    def remove_comment(self, comment):
        """Remove a comment from the post and decrement the comments_count."""
        self.comments.remove(comment)
        self.comments_count -= 1
        db.session.commit()

    


# Model Schema for Comment Table
class Comment(db.Model):
    """This Class defines the Comment Model"""

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """This Function returns a String Representation"""

        return f"<Comment {self.body[:20]}>"