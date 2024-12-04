"""This file is a Form class that has the attributes recieved byt eh flask form and validates them. Includes Many Forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# Form to Add Post
class AddPostForm(FlaskForm):
    """This Class defines The Add post form fields"""

    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    code_snippet = TextAreaField('Code Snippet')
    submit = SubmitField('Submit Post')

# Form to Signup User, Includes validation and shows user messages if failed validation
class SignupForm(FlaskForm):
    """This Class defines The Singup Form Fields"""
    
    firstname = StringField(
        'First Name', 
        validators=[
            DataRequired(message="First name is required."),
            Length(max=50, message="First name must not exceed 50 characters.")
        ]
    )
    lastname = StringField(
        'Last Name', 
        validators=[
            DataRequired(message="Last name is required."),
            Length(max=50, message="Last name must not exceed 50 characters.")
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(message="Confirm password is required."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message="Username is required."),
            Length(max=50, message="Username must not exceed 50 characters.")
        ]
    )
    submit = SubmitField('Sign Up')

# Form to Login Users
class LoginForm(FlaskForm):
    """This Class defines The Login Form Fields"""
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# Form to Udate Name, Includes Server Side Validation
class UpdateNameForm(FlaskForm):
    firstname = StringField('First Name', validators=[
        DataRequired(), Length(max=50, message="First name must be less than 50 characters.")
    ])
    lastname = StringField('Last Name', validators=[
        DataRequired(), Length(max=50, message="Last name must be less than 50 characters.")
    ])
    submit = SubmitField('Update Name')

# Form to Update Email, Includes Server Side Validation
class UpdateEmailForm(FlaskForm):
    """This Class defines The Update Form Fields"""
    
    email = StringField('Email', validators=[
        DataRequired(), Email(message="Enter a valid email address.")
    ])
    confirm_email = StringField('Confirm Email', validators=[
        DataRequired(), Email(message="Enter a valid email address."),
        EqualTo('email', message="Emails must match.")
    ])
    submit = SubmitField('Update Email')

# Form to Update Password, Includes Server Side Validation
class UpdatePasswordForm(FlaskForm):
    """This Class defines The Update Password Form"""
    
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message="Passwords must match.")
    ])
    submit = SubmitField('Update Password')

# Form to Update Username, Includes Server Side Validation
class UpdateUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[
        DataRequired(), Length(max=80, message="Username must be less than 80 characters.")
    ])
    confirm_username = StringField('Confirm Username', validators=[
        DataRequired(), EqualTo('username', message="Usernames must match.")
    ])
    submit = SubmitField('Update Username')

# Form for Logging in user, Includes validation
class LoginForm(FlaskForm):
    """This Class defines The Login Form Fields"""
    
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=128)
    ])
    submit = SubmitField('Log In')