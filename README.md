# Trivia API


## Full Stack Trivia


This project is a vritual trivia. Users are able to create, add and delete questions and their respective answers. Users also have a section to practice with random questions where it's possible to select an individual category.


## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

#### Frontend
From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable


### Endpoints

```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```


```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
- Sample: `curl -X POST -H 'Content-Type: application/json' -d '{"previous_questions":[], "quiz_category": 1}' http://127.0.0.1:5000/quizzes`
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
- Sample: `curl -X POST -H 'Content-Type: application/json' -d '{"question": "new question", "answer": "new answer", "difficulty": 1, "category": 1}' http://127.0.0.1:5000/questions`
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
- Returns: Does not return any new data
```

```js
POST '/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
- Sample: `curl -X POST -H 'Content-Type: application/json' -d '{"searchTerm": "movie"}' http://127.0.0.1:5000/questions`
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```



