"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class TestUserViewTestcase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_show_home(self):
        """should show empty screen"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/")
            html = resp.get_data(as_text=True)
            # Make sure it redirects
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Sign up now to get your own personalized timeline!',html)

    def test_show_anon_home(self):
        """should show empty screen"""

        with self.client as c:

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/")
            html = resp.get_data(as_text=True)
            # Make sure it redirects
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sign up now to get your own personalized timeline!',html)
