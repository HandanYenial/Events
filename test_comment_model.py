import os 
#OS module in Python provides functions for interacting with the
#operating system. OS comes under Python’s standard utility modules.
#This module provides a portable way of using operating system dependent
#functionality

from unittest import TestCase
from sqlalchemy import exc #sqlalchemy exceptions

from models import db, User, Comment, Event, Wishlist

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///event_test" #modify the environmet variable


#os.environ in Python is a mapping object that represents the user’s environmental 
#variables. It returns a dictionary having user’s environmental variable as key and 
#their values as value.os.environ behaves like a python dictionary, so all the common
#dictionary operations like get and set can be performed. 

# Now we can import app


# run these tests like:
#
# python -m unittest test_comment_model.py

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for comments."""

    def setUp(self):
        """Create test client,add sample data"""
        db.drop_all()
        db.create_all()

        self.uid = 123456
        u = User.signup("user1" , "testing@test.com" , "password", "image.url","userfirst","userlast")
        u.id = self.uid

        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_comment_model(self):
        """Does basic model work"""

        c = Comment(
        text = "a comment",
        user_id = self.uid
    )

        db.session.add(c)
        db.session.commit()


