import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('DB_NAME', 'trivia_test')
        self.database_user = os.getenv('DB_USER', 'postgres')
        self.database_password = os.getenv('DB_PASSWORD', 'postgres')
        self.database_host = os.getenv('DB_HOST', '127.0.0.1:5432')

        self.database_path = "postgres://{}/{}".format(
            self.database_host,
            self.database_name
        )

        # self.database_path = 'postgresql://{}:{}@{}/{}'.format(
        #     self.database_user,
        #     self.database_password,
        #     self.database_host,
        #     self.database_name)

        setup_db(self.app, self.database_path)

        # use to create
        # new question
        self.new_data = {
            "question": "Heres a new question string",
            "answer": "Heres a new answer string",
            "difficulty": 1,
            "category": 3
        }

        self.search_data = {
            "searchTerm": "this is the term the user is looking for",
        }

        self.quiz_data = {
            "previous_questions": [1, 8, 2],
            "quiz_category": {"type": "Science", "id": "1"},
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('http://127.0.0.1:5000/categories')
        res_data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data["categories"])

    def test_405_get_categories(self):
        res = self.client().post('http://127.0.0.1:5000/categories')
        res_data = res.get_json()

        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get(f'http://127.0.0.1:5000/questions?page={0}')
        res_data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data["totalQuestions"])
        self.assertTrue(res_data["categories"])
        self.assertTrue(len(res_data["questions"]))

    def test_422_get_questions(self):
        res = self.client().get(
            f'http://127.0.0.1:5000/questions?page={"one"}')
        res_data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertFalse(res_data["success"])
        self.assertEqual(res_data["message"], "Unprocessable")

    def _test_delete_question(self):
        res = self.client().delete("http://127.0.0.1:5000/questions/6")
        res_data = res.get_json()

        self.assertEqual(res.status_code, 200)

    def test_500_delete_question(self):
        res = self.client().delete("http://127.0.0.1:5000/questions/1000")
        res_data = res.get_json()

        self.assertEqual(res.status_code, 500)
        self.assertFalse(res_data["success"])
        self.assertEqual(res_data["message"], "Internal Sever Error")

    def test_add_question(self):
        res = self.client().post("http://127.0.0.1:5000/questions",  json=self.new_data)
        res_data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)

    def test_405_if_add_question_not_allowed(self):
        res = self.client().post("http://127.0.0.1:5000/questions/455",  json=self.new_data)
        res_data = res.get_json()

        self.assertEqual(res.status_code, 405)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Method Not Allowed")

    def test_search_question(self):
        res = self.client().post(
            "http://127.0.0.1:5000/questions?action=search",  json=self.search_data)
        self.assertEqual(res.status_code, 200)

    def test_422_search_question(self):
        res = self.client().get(
            "http://127.0.0.1:5000/questions?action=search",  json=self.search_data)
        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):
        res = self.client().get("http://127.0.0.1:5000/categories/3/questions")
        res_data = res.get_json()
        self.assertEqual(res.status_code, 200)

    def test_405_get_questions_by_category(self):
        res = self.client().post("http://127.0.0.1:5000/categories/3/questions")
        self.assertEqual(res.status_code, 405)

    def test_get_quizzess(self):
        res = self.client().post("http://127.0.0.1:5000/quizzes", json=self.quiz_data)
        res_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data["question"])

    def test_400_get_quizzess(self):
        res = self.client().post("http://127.0.0.1:5000/quizzes")
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
