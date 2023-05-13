"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from datetime import datetime

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(self.u)
        db.session.commit()
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        db.session.commit()
    
    def test_create_message(self):
        """Does basic model work?"""
        message = Message(
            text = "a",
            user_id = self.u.id
        )

        db.session.add(message)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(message.text, "a")
        self.assertEqual(message.user_id, self.u.id)
        self.assertIsInstance(message.timestamp, datetime)

    def test_create_fail(self):
        """delete cascade"""        
        message = Message(
            text = "a",
            user_id = self.u.id
        )

        db.session.add(message)
        db.session.commit()

        User.query.delete()
        db.session.commit()
        self.assertEqual(len(Message.query.all()),0)