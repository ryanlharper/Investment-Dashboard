from flask import Blueprint, jsonify, abort, request
from ..models import Category, db

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('', methods=['GET'])
def index():
    categories = Category.query.all() 
    result = []
    for c in categories:
        result.append(c.serialize()) # build list of Categories as dictionaries
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    c = Category.query.get_or_404(id)
    return jsonify(c.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)
    c = Category(
        name=request.json['name']
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

"""@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    name = data.get('name', category.name)
    category.name = name
    db.session.commit()
    return jsonify(category.serialize()), 200
"""
