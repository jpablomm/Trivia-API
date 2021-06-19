import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    """Fetch and return all categories. Pagination not required."""

    data = {
      'categories': {}
    }
    try:
      categories = Category.query.order_by(Category.id).all()
      for category in categories:
        data['categories'][f'{category.id}'] = f'{category.type}'

      return jsonify(data), 200
    except Exception:
      abort(404)


  @app.route('/questions')
  def get_questions():
    """Fetch and return paginated questions."""

    page_id = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()

    questions_per_page = 10
    start = (page_id - 1) * questions_per_page
    end = start + questions_per_page

    data = {
      'questions': [],
      'totalQuestions': len(questions),
      'categories': {},
      'currentCategory': None
    }

    for question in questions[start:end]:
      data['questions'].append(question.format())

    if len(data['questions']) == 0:
      abort(422)

    for category in categories:
      data['categories'][f'{category.id}'] = f'{category.type}'
    return jsonify(data)


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """Fetch and delete question."""
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)
    question_id = question.id
    Question.delete(question)

    return jsonify({'deleted': question_id}), 200


  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()
    search = data.get('searchTerm', None)
    if search:
      questions = Question.query \
        .filter(Question.question.ilike('%{}%'.format(data['searchTerm']))).all()
      res = {
        'questions': [],
        'totalQuestions': len(questions),
        'currentCategory': None
      }
      for question in questions:
        new_question = {
          'question': question.question,
          'answer': question.answer,
          'difficulty': question.difficulty,
          'category': question.category
        }
        res['questions'].append(new_question)
      return jsonify(res)
    else:
      new_question = Question(
        question = data.get('question'),
        answer = data.get('answer'),
        difficulty = int(data.get('difficulty')),
        category = int(data.get('category'))
      )
      print(new_question)
      try:
        new_question.insert()
        return jsonify({}), 200
      except Exception:
        print(Exception)
        abort(422)


  @app.route('/categories/<int:category_id>/questions')
  def get_question_based_on_category(category_id):
    """Fetch and serve questions based on category."""
    try:
      questions = Question.query.filter(Question.category == category_id).all()
      res = {
          'questions': [],
          'totalQuestions': len(questions),
          'currentCategory': Category.query.filter(Category.id == category_id).first().type
        }
      for question in questions:
        new_question = {
          'question': question.question,
          'answer': question.answer,
          'difficulty': question.difficulty,
          'category': question.category
        }
        res['questions'].append(new_question)

      return jsonify(res), 200
    except Exception:
      abort(404)


  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    """Select and send random questions in specific category."""
    data = request.get_json()
    try:
      previous_questions = data.get('previous_questions', None)
      quiz_category_id = data.get('quiz_category', None)['id']
      if quiz_category_id == 0:
        cat_questions = Question.query.all()
      else:
        cat_questions = Question.query.filter(Question.category == int(quiz_category_id)).all()

      questions = [question for question in cat_questions if question.id not in previous_questions]

      random_question = random.choice(questions)

      res = {
        'question': {
          'id':random_question.id,
          'question': random_question.question,
          'answer': random_question.answer,
          'difficulty': random_question.difficulty,
          'category': random_question.category
        }
      }
      return jsonify(res), 200
    except:
      abort(404)


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404


  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422


  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400


  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not alowed'
    }), 405

  return app
