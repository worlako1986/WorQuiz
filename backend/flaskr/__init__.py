import os
from re import T
from unicodedata import category
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

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        try:
            return jsonify({
                "success": True,
                "categories": load_categories()
            })
        except Exception as e:
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of 
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        try:

            # Paginate
            start = int(request.args.get("page"))
            end = start + QUESTIONS_PER_PAGE

            # load questions
            questions_query = Question.query.all()[start: end]
            questions = [question.format() for question in questions_query]
            categories = load_categories()
            current_category_id = get_current_category_id()

            return jsonify({
                "success": True,
                "questions": questions,
                "totalQuestions": Question.query.count(),
                "categories": categories,
                "currentCategory": categories[current_category_id]
            })

        except Exception as e:
            abort(422)

    def load_categories():
        categories_query = Category.query.all()
        # format data
        return {category.id: category.type for category in categories_query}

    def get_current_category_id():
        total_category = Category.query.count()
        return random.randint(1, total_category)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, 
    the question will be removed.
    This removal will persist in the database and 
    when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                "success": True,
                "question_id": question_id,
            })
        except Exception as e:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will 
    appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def add_and_search_questions():
        """ Add new questions and search questions
        using submited data
        """
        try:
            if request.args.get("action", "") == "search":
                # Search questions with search_term
                search_term = request.get_json()["searchTerm"]
                return jsonify(search_question(search_term))

            else:
                # Add new question
                request_data = request.get_json()
                question = Question(
                    question=request_data["question"],
                    answer=request_data["answer"],
                    category=request_data["category"],
                    difficulty=request_data["difficulty"],
                )

                question.insert()
                return jsonify({
                    "success": True
                })
        except Exception as e:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    def search_question(search_term):
        # Retrieve match question
        questions_query = Question.query.filter(
            Question.question.ilike("%"+search_term+"%"))
        questions = [question.format() for question in questions_query]
        category = Category.query.get(get_current_category_id())

        return {
            "questions": questions,
            "totalQuestions": len(questions),
            "currentCategory": category.type
        }

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<string:category_id>/questions')
    def get_question_by_category(category_id):
        try:
            questions_query = Question.query.filter(
                Question.category == category_id)
            questions = [question.format() for question in questions_query]
            category = Category.query.get(get_current_category_id())

            return jsonify({
                "questions": questions,
                "totalQuestions": len(questions),
                "currentCategory": category.type
            })
        except Exception as e:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=["POST"])
    def get_quezzes():
        try:
            request_data = request.get_json()
            previous_questions = request_data["previous_questions"]
            quiz_category = request_data["quiz_category"]

            # Load quizzess
            quizzes_query = []
            if int(quiz_category["id"]) == 0:
                # Load all question
                quizzes_query = Question.query.\
                    filter(Question.id.not_in(previous_questions))
            else:
                quizzes_query = Question.query.\
                    filter(Question.category == quiz_category["id"]).\
                    filter(Question.id.not_in(previous_questions))

            # Format quizzes
            quizzes = [quiz.format() for quiz in quizzes_query]
            # Get current quiz index
            quiz_index = random.randint(0, len(quizzes) - 1)

            return jsonify({
                "success": True,
                "question": quizzes[quiz_index]
            })
        except Exception as e:
            print(str(e))
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "Unprocessable"}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Sever Error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
