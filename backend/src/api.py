from asyncio.base_subprocess import ReadSubprocessPipeProto
import os
from flask import Flask, request, jsonify, abort
from numpy import recarray, require
from pyrsistent import s
from soupsieve import select
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
import ssl

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def get_drinks():

    selections = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in selections]
    return jsonify(
        {
            "success": True,
            "drinks": drinks
            }
        )

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure

'''


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    # selection = Drink.query.filter(Drink.id == id).one_or_none()]
    selection = Drink.query.all()
    drinks = [drink.long() for drink in selection]
    return jsonify(
        {
            "success": True,
            "drinks": drinks
        })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()

    if 'title' and 'recipe' not in body:
        abort(422)
    
    title = body['title']
    recipe = json.dumps(body['recipe'])
    new_drink = Drink(title=title, recipe=recipe)
    try:
        new_drink.insert()
    except:
        print("can't add new drink")
        abort(500)
    return jsonify(
        {
            "success": True,
            "drink": [new_drink.long()]
        }
    )
      

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    drink = Drink.query.filter_by(id=id).one_or_none()
    if drink is None:
        abort(404)
    try:
        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            drink.recipe = body['recipe'] 
        drink.update()
    except:
        print("could not update drink")
        abort(500)
    return jsonify(
        {
            "success": True,
            "drinks": [drink.long()]
        }
    )

    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get_or_404(id)
    try:
        drink.delete()
    except:
        abort(500)

    return jsonify(
        {
            "success": True,
            "delete": id
        }
    )
    

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

