#NEEDS to be updated since migration/integration

from flask import Blueprint, jsonify, abort, request
from ..models import User, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])
def index():
    users = User.query.all() 
    result = []
    for u in users:
        result.append(u.serialize()) 
    return jsonify(result) 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password=scramble(request.json['password'])


    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required.'}), 400
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    username = data.get('username', user.username)
    email = data.get('email', user.email)
    password = data.get('password', user.password)
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required.'}), 400
    user.username = username
    user.email = email
    user.password = password
    db.session.commit()
    return jsonify(user.serialize()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
