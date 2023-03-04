from flask import Blueprint, jsonify, abort, request
from ..models import Subcategory, Category, db

bp = Blueprint('subcategories', __name__, url_prefix='/subcategories')

@bp.route('', methods=['GET']) 
def index():
    subcategories = Subcategory.query.all()
    result = []
    for sc in subcategories:
        result.append(sc.serialize()) # build list of Subcategories as dictionaries
    return jsonify(result) 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    sc = Subcategory.query.get_or_404(id)
    return jsonify(sc.serialize())

@bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    name = data.get('name')
    category_id = data.get('category_id')
    # Check that all required fields are present
    if name is None or category_id is None:
        return abort(400, "Missing required fields")
    # Check that category_id corresponds to an existing category
    category = Category.query.get(category_id)
    if category is None:
        return abort(400, "Invalid category_id")
    # Create a new subcategory
    subcategory = Subcategory(name=name, category_id=category_id)
    db.session.add(subcategory)
    db.session.commit()
    return jsonify(subcategory.serialize(subcategory)), 201

"""@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    subcategory = Subcategory.query.get_or_404(id)
    data = request.get_json()
    name = data.get('name', subcategory.name)
    subcategory.name = name
    db.session.commit()
    return jsonify(subcategory.serialize()), 200"""

