"""In-memory, unserved Flask/SQLite regression checks; no external services."""
import unittest
from server.webapp import flaskapp, database, cursor
import server.routes

class SearchRegression(unittest.TestCase):
    def setUp(self):
        flaskapp.config.update(TESTING=True)
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("CREATE TABLE books (name text, author text, read text)")
        cursor.executemany("INSERT INTO books VALUES (?, ?, ?)", [
            ("Alpha", "Ada", "false"),
            ("Beta", "Bob", "true"),
            ("O'Reilly", "Carol", "false"),
        ])
        database.commit()
        self.client = flaskapp.test_client()

    def test_default_listing(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alpha", response.data)
        self.assertIn(b"Beta", response.data)

    def test_name_search(self):
        response = self.client.get("/", query_string={"name": "Alpha"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alpha", response.data)
        self.assertNotIn(b"Beta", response.data)

    def test_author_search(self):
        response = self.client.get("/", query_string={"author": "Ada"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Alpha", response.data)
        self.assertNotIn(b"Beta", response.data)

    def test_quote_is_data(self):
        response = self.client.get("/", query_string={"name": "O'Reilly"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"O&#39;Reilly", response.data)

    def test_name_injection_is_data(self):
        response = self.client.get("/", query_string={"name": "' OR 1=1 --"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Alpha", response.data)
        self.assertNotIn(b"Beta", response.data)

    def test_author_injection_is_data(self):
        response = self.client.get("/", query_string={"author": "' OR 1=1 --"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Alpha", response.data)
        self.assertNotIn(b"Beta", response.data)

if __name__ == "__main__":
    unittest.main()
