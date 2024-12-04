"""This file is a a Unit Testing File containing Tests to show the application is working correctly."""

import unittest
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app_context = app.app_context()
        self.app_context.push()

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        db.create_all()

        # Create a test user
        self.user = models.User(
            firstname="Test",
            lastname="User",
            email="testuser@example.com",
            username="testuser"
        )
        self.user.set_password("password123")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        """Test if the home route is accessible."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """Test creating a new user."""

        # Create a New User
        user = models.User(
            firstname="Jane",
            lastname="Doe",
            email="janedoe@example.com",
            username="janedoe"
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # Fetch User and Validate
        fetched_user = models.User.query.filter_by(username="janedoe").first()
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.email, "janedoe@example.com")

    def test_add_post(self):
        """Test adding a new post."""

        # Add a New Post
        post = models.Post(
            title="Test Post",
            body="This is a test post body.",
            user_id=self.user.id
        )
        db.session.add(post)
        db.session.commit()

        # Try Find the Post
        fetched_post = models.Post.query.filter_by(title="Test Post").first()
        self.assertIsNotNone(fetched_post)
        self.assertEqual(fetched_post.body, "This is a test post body.")

    def test_add_comment(self):
        """Test adding a comment to a post."""

        # Create a Post
        post = models.Post(
            title="Test Post",
            body="This is a test post body.",
            user_id=self.user.id
        )
        db.session.add(post)
        db.session.commit()

        # Create a Comment
        comment = models.Comment(
            body="This is a test comment.",
            post_id=post.id,
            user_id=self.user.id
        )
        db.session.add(comment)
        db.session.commit()

        # Fetch the Comment and check if it is there
        fetched_comment = models.Comment.query.filter_by(body="This is a test comment.").first()
        self.assertIsNotNone(fetched_comment)
        self.assertEqual(fetched_comment.body, "This is a test comment.")
        self.assertEqual(fetched_comment.post.id, post.id)

    def test_like_post(self):
        """Test liking a post."""

        # Create a Post
        post = models.Post(
            title="Test Post",
            body="This is a test post body.",
            user_id=self.user.id
        )
        db.session.add(post)
        db.session.commit()

        # Like a Post
        self.user.like_post(post)
        db.session.commit()

        # Check if post is liked
        self.assertTrue(self.user.has_liked_post(post))
        self.assertEqual(post.liked_by.count(), 1)

    def test_unlike_post(self):
        """Test unliking a post."""

        # Create a Post
        post = models.Post(
            title="Test Post",
            body="This is a test post body.",
            user_id=self.user.id
        )
        db.session.add(post)
        db.session.commit()

        # Like and Unlike Post
        self.user.like_post(post)
        db.session.commit()
        self.user.unlike_post(post)
        db.session.commit()

        # Check if Post is still licked
        self.assertFalse(self.user.has_liked_post(post))
        self.assertEqual(post.liked_by.count(), 0)

    def test_follow_user(self):
        """Test following another user."""

        # Create User
        other_user = models.User(
            firstname="John",
            lastname="Doe",
            email="johndoe@example.com",
            username="johndoe"
        )
        other_user.set_password("password123")  # Set password
        db.session.add(other_user)
        db.session.commit()

        # Follow User
        self.user.follow(other_user)
        db.session.commit()

        # Check if user is following and other user is followed by
        self.assertTrue(self.user.is_following(other_user))
        self.assertTrue(other_user.is_followed_by(self.user))

    def test_unfollow_user(self):
        """Test unfollowing another user."""

        # Create User with password
        other_user = models.User(
            firstname="John",
            lastname="Doe",
            email="johndoe@example.com",
            username="johndoe"
        )
        other_user.set_password("password123")  # Set password
        db.session.add(other_user)
        db.session.commit()

        # Follow and Unfollow and Check if it works
        self.user.follow(other_user)
        db.session.commit()
        self.user.unfollow(other_user)
        db.session.commit()

        self.assertFalse(self.user.is_following(other_user))
        self.assertFalse(other_user.is_followed_by(self.user))

    


if __name__ == '__main__':
    unittest.main()