#NEEDS to be updated since migration/integration

from flask import Blueprint, jsonify, abort, request
from ..models import Budget, db

bp = Blueprint('budget_items', __name__, url_prefix='/budget_items')

@bp.route('', methods=['GET']) 
def index():
    budgets = Budget.query.all() 
    result = []
    for b in budgets:
        result.append(b.serialize()) # build list of Budget Items as dictionaries
    return jsonify(result) 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = Budget.query.get_or_404(id)
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    data = request.json
    amount = data.get('amount')
    year_id = data.get('year_id')
    category_id = data.get('category_id')
    subcategory_id = data.get('subcategory_id')
    user_id = data.get('user_id')
    if not all([amount, year_id, category_id, subcategory_id, user_id]):
        # If any of the required fields are missing from the request, return a 400 Bad Request error
        return abort(400)
    try:
        budget = Budget(amount=amount, year_id=year_id, category_id=category_id, subcategory_id=subcategory_id, user_id=user_id)
        db.session.add(budget)
        db.session.commit()
        return jsonify(budget.serialize()), 201 
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to create budget item.'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    budget_item = Budget.query.get_or_404(id)
    db.session.delete(budget_item)
    db.session.commit()
    return jsonify(True)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    budget = Budget.query.get_or_404(id)
    if request.method == 'PATCH':
        # update only the fields provided in the request
        amount = request.json.get('amount', budget.amount)
        year_id = request.json.get('year_id', budget.year_id)
        category_id = request.json.get('category_id', budget.category_id)
        subcategory_id = request.json.get('subcategory_id', budget.subcategory_id)
        user_id = request.json.get('user_id', budget.user_id)
        budget.amount = amount
        budget.year_id = year_id
        budget.category_id = category_id
        budget.subcategory_id = subcategory_id
        budget.user_id = user_id
    elif request.method == 'PUT':
        # update all the fields in the request
        budget.amount = request.json['amount']
        budget.year_id = request.json['year_id']
        budget.category_id = request.json['category_id']
        budget.subcategory_id = request.json['subcategory_id']
        budget.user_id = request.json['user_id']
    db.session.commit()
    return jsonify(budget.serialize())
