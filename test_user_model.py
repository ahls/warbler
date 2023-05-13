"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        db.session.commit()
        
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_follow(self):
        """Does is_following successfully detect when user1 is following user2"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)

        u2 = User(
            email="test1@test.com",
            username="1testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        follow = Follows(
            user_being_followed_id=u1.id,
            user_following_id=u2.id
        )

        db.session.add(follow)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u1.followers), 1)
        self.assertEqual(len(u2.followers), 0)
        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u2.following), 1)

    def test_user_unfollow(self):
        """Does is_following successfully detect when user1 is not following user2"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)

        u2 = User(
            email="test1@test.com",
            username="1testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        follow = Follows(
            user_being_followed_id=u1.id,
            user_following_id=u2.id
        )

        db.session.add(follow)
        db.session.commit()
        self.assertEqual(len(u1.followers), 1)
        self.assertEqual(len(u2.followers), 0)
        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u2.following), 1)

        db.session.delete(follow)
        db.session.commit()
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u2.followers), 0)
        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u2.following), 0)

    def test_user_create(self):
        """Does user.signup work?"""

        u = User.signup(
            username="aww",
            email="test@test.com",
            password = "123123",
            image_url = ""
            )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_create_failcase(self):
        """Does user.signup work?"""

        u = User.signup(
            username="aww",
            email="test@test.com",
            password = "123123",
            image_url = ""
            )

        db.session.add(u)
        db.session.commit()

        with self.assertRaises(Exception):
            dupName = User.signup(
                username="aww",
                email="teswt@test.com",
                password = "123123",
                image_url = ""
                )
            db.session.add(dupName)
            db.session.commit()

        with self.assertRaises(Exception):
            dupEmail = User.signup(
                username="aww2",
                email="test@test.com",
                password = "123123",
                image_url = ""
                )
            db.session.add(dupEmail)
            db.session.commit()

        with self.assertRaises(Exception):

            shortPW = User.signup(
                username="aww3",
                email="test3@test.com",
                password = "1",
                image_url = ""
                )
            db.session.add(shortPW)
            db.session.commit()

        db.session.rollback()
        userCount = len(User.query.all())
        # User should have no messages & no followers
        self.assertEqual(userCount, 1)

