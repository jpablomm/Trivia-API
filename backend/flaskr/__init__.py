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
  
  '''
  @(DONE)TODO(DONE): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @(DONE)TODO(DONE): Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

  '''
  @(DONE)TODO(DONE): 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
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

  '''
  @(DONE)TODO(DONE): 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
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


  '''
  @(DONE)TODO(DONE): 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """Fetch and delete question."""
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    if question is None:
      abort(404)
    question_id = question.id
    Question.delete(question)

    return jsonify({'deleted': question_id}), 200


  '''
  @(DONE)TODO(DONE): 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
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

  '''
  @(DONE_ABOVE)TODO(DONE_ABOVE): 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_question_based_on_category(category_id):
    questions = Question.query.filter(Question.category == category_id).first()
    res = {
        'questions': [],
        'totalQuestions': len(questions),
        'currentCategory': Category.query.filter(Category.id == category_id).first()
      }
    for question in questions:
      new_question = {
        'question': question.get('question'),
        'answer': question.get('answer'),
        'difficulty': question.get('difficulty'),
        'category': question.get('category')
      }
      res['questions'].append(new_question)

      return jsonify(res), 200

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @(DONE)TODO(DONE):
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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

    