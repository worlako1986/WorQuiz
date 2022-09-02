## API Reference

### Getting Started

- Base url: The trivia app currently runs locally.
  The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Client library: python

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

### Http Status Code Summary

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error
- 405: Method Not Allow

### Endpoints

#### GET /categories

- General:
  - Returns a json representation of category objects, and success value
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions?page=0

- General:
  - Returns a list of question objects, categories, current category, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 0.
- Sample: `curl http://127.0.0.1:5000/questions?page=0`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 6,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 7,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 8,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 9,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 12,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "totalQuestions": 19
}

```

#### DELETE /questions/<int:question_id>

- General:
  - Delete specific question by the id, Return question id, and success value
- Sample: `curl http://127.0.0.1:5000/questions/1`

```
{
  "success": true,
  "question_id": 1
}
```

#### POST /questions

- General:
  - Creates a new question using the submitted question, category, answer and difficulty and Returns success value.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "answer": "The Palace of Versailles", "category": "3", "difficulty": 3, "question": "In which royal palace would you find the Hall of Mirrors?" }'`

```
{
  "success": true,
}
```

#### POST /questions

- General:
  - Search questions by any phrase using the submitted request body.
  - Return the list question objects base on the search phrase, total question, current category and success value.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "search_term": "which", "action": "search" }'`

```
{
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 6,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 7,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 12,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "totalQuestions": 19
  "currentCategory": "Art"
}

```

#### GET /categories/1/questions

- General:
  - Returns a list of question objects base on selected category, success value, and total number of questions.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 15,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 16,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 17,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "dd",
      "category": "1",
      "difficulty": 1,
      "id": 24,
      "question": "Question"
    }
  ],
  "totalQuestions": 4
}

```

#### POST /quizzes

- General:
  - Return a random questions within the given category,
    if provided, and that is not one of the previous questions.
  - Request body: { "previous_questions": [1, 8, 2], "quiz_category": {"type": "Science", "id": "1"}
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [1, 8, 2], "quiz_category": {"type": "Science", "id": "1"}, }'`

```
{
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 12,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true
}

```
