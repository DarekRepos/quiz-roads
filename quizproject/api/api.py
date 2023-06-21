from flask import Blueprint, jsonify, json
from . import question_api

"""
    view swagger
    ✅ GET /Questions: lists of all questions titles .
    ✅ GET /Questions: lists of all questions with answers.
    ✅ GET /Answers{questionid}/question: lists of all answers.

    ✅ GET /questions/{questionid}: get quetioon
    
    ✅ GET /questions: lists of all questions with pagination..
    
    ✅ GET /users/{userId}/quiz : lists of all orders for a particular user.
    ✅ POST /users: creates a new user.
    ✅ PUT /users/{userId}: updates a user.
    ✅ DELETE /users/{userId}: deletes a specific user.
    ✅ PATCH /users/{userId}: partially updates a user.
    ✅ POST /users/{userId}/cart/checkout: runs the checkout process.

    protect routes with flask-api-key

"""


@question_api.route("/questions", methods=["GET"])
# @swag_from()
def get_all_questions():
    """
    question = {
        'id': 1,
        'fromquizid': [2, 3]
        'dificulty': 5,
        'text': 'question text',
        'multianswer': 0,
        'isactive': 1
    }
       result = {
        'question1': ['answer1', 'answer2', 'answer3', 'answer4'],
        'question2': ['yes', 'no'],
        'question3': : ['answer1', 'answer2', 'answer3', 'answer4', 'answer4'],
    }

    Returns:
        _type_: _description_
    """
    result = 1
    return jsonify(result)
