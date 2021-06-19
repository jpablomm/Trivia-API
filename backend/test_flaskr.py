import os
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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996? ',
            'answer': 'Apollo 13',
            'difficulty': 4,
            'category': 5
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(data['categories'])


    def test_paginated_questions(self):
        res = self.client().get('questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(len(data['categories']), 6)


    def test_404_with_wrong_questions_page(self):
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """
    def test_detele_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 2)
    """

    def test_detele_question_that_do_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)

        self.assertEqual(res.status_code, 200)


    def test_create_question_wrong_url(self):
        res = self.client().post('/questions/550', json=self.new_question)

        self.assertEqual(res.status_code, 405)


    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'country'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 1)


    def test_search_questions_wrong(self):
        res = self.client().post('/questions', json={'searchTerm': 'sñghfsalgfd'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 4)


    def test_questions_by_category_nonexistent(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


    def test_quizz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': '1'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])


    def test_quizz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': '100000'
        })

        self.assertEqual(res.status_code, 404)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()