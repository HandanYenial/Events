
#    FLASK_ENV=production python -m unittest test_comment_views.py


import os
from unittest import TestCase

from models import db, connect_db, Comment, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///event_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class CommentViewTestCase(TestCase):
    """Test views for comments."""

    def setUp(self):
        """Create test client, add sample data."""

       # User.query.delete()
        Comment.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser2",
                                    email="test@test2.com",
                                    password="testuse2r",
                                    img_url=None,
                                    first_name="first",
                                    last_name = "last")

        self.testuser_id = 891223
        self.testuser.id = self.testuser_id

        db.session.commit()

    def test_add_comment(self):

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/comments/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 200)

            comm = Comment.query.one()
            self.assertEqual(comm.text, "Hello")

#sqlalchemy.exc.NoResultFound: No row was found when one was required

    def test_add_no_session(self):
        with self.client as c:
            resp = c.post("/comments/new" , data={"text":"Hello"})
            self.assertEqual(resp.status_code,200)
            self.assertIn("Access unauthorized" , str(resp.data))
