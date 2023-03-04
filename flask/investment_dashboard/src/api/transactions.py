from flask import Blueprint, jsonify, abort, request
from ..models import Transaction, User, db

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    transactions = Transaction.query.all() # ORM performs SELECT query
    result = []
    for t in transactions:
        result.append(t.serialize()) # build list of Transactions as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Transaction.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'user_id' not in request.json or 'amount' not in request.json: # req body must contain user_id and amount
        return abort(400)
    User.query.get_or_404(request.json['user_id']) # user with id must exist
    # construct Transaction
    t = Transaction(
        amount=request.json['amount'],
        date = request.json['date'],
        category_id = request.json['category_id'],
        subcategory_id = request.json['subcategory_id'],
        user_id= request.json['user_id'],
        description = request.json['description']
    )
    db.session.add(t) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(t.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Transaction.query.get_or_404(id)
    try:
        db.session.delete(t) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        return jsonify(False)

@bp.route('/<int:id>', methods=['PUT'])
def update_transaction(id: int):
    t = Transaction.query.get_or_404(id)
    # Get updated values from request body
    req_data = request.get_json()
    new_amount = req_data.get('amount')
    new_description = req_data.get('description')
    new_date = req_data.get('date')
    new_category = req_data.get('category')
    new_subcategory_id = req_data.get('subcategory_id')
    # Update transaction with new values
    t.amount = new_amount
    t.description = new_description
    t.date = new_date
    t.category = new_category
    t.subcategory_id = new_subcategory_id
    # Commit changes to database
    db.session.commit()
    return jsonify(t.serialize())

@bp.route('/<int:id>', methods=['PATCH'])
def patch_transaction(id: int):
    t = Transaction.query.get_or_404(id)
    # Update transaction with new values from request body
    req_data = request.get_json()
    for key, value in req_data.items():
        if key == 'amount':
            t.amount = value
        elif key == 'description':
            t.description = value
        elif key == 'date':
            t.date = value
        elif key == 'category':
            t.category = value
        elif key == 'subcategory_id':
            t.subcategory_id = value
    # Commit changes to database
    db.session.commit()
    return jsonify(t.serialize())
