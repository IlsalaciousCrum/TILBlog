import unittest

from server import app
from model import db, example_data, connect_to_db

#  ------------------------------------


class TILTestsRoutes(unittest.TestCase):
    """Tests for TILBlog site."""

    def setUp(self):
        """Stuff to do before every route test."""


class TILTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every database test."""

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_some_db_thing(self):
        """Some database test..."""

        pass

    def test_some_flask_route(self):
        """Some non-database test..."""

        result = self.client.get("/my-route")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Test</h1>', result.data)

    def test_login(self):
        result = self.client.post("/login",
                                  data={"user_id": "rachel", "password": "123"},
                                  follow_redirects=True)
        self.assertIn("You are a valued user", result.data)

#  --------------------------------------

if __name__ == "__main__":
    unittest.main()
