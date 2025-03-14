from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from app.database import get_collection
from bson.objectid import ObjectId
from app.models.user import User, UserPreferences
from datetime import datetime
from dataclasses import asdict


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def health_check() -> Response:
    return jsonify({"status": "healthy"}), 200


@app.route('/users', methods=['GET'])
def get_users() -> Response:
    users = get_collection('users').find()
    users_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        users_list.append(user)
    return jsonify(users_list)


@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id: str) -> Response:
    user = get_collection('users').find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user['_id'] = str(user['_id'])
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user() -> Response:
    user_data = request.json
    
    user = get_collection('users').find_one({'username': user_data.get('username')})
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    user_obj = User(
        username=user_data.get('username'),
        password=user_data.get('password'),
        roles=user_data.get('roles', []),
        preferences=UserPreferences(timezone=user_data.get('timezone', 'UTC')),
        active=user_data.get('active', True),
        created_ts=user_data.get('created_ts', datetime.now().timestamp())
    )
    
    user_dict = asdict(user_obj)
    result = get_collection('users').insert_one(user_dict)
    if not result.inserted_id:
        return jsonify({'error': 'User not created'}), 400
    
    user_dict.pop('password', None)
    user_dict['_id'] = str(result.inserted_id)

    return jsonify(user_dict), 201


@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id: str) -> Response:
    user_data = request.json
    user = get_collection('users').find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_obj = User(
        username=user_data.get('username'),
        password=user_data.get('password'),
        roles=user_data.get('roles', []),
        preferences=UserPreferences(timezone=user_data.get('timezone', 'UTC')),
        active=user_data.get('active', True),
        created_ts=user_data.get('created_ts', datetime.now().timestamp())
    )
    user_dict = asdict(user_obj)
    result = get_collection('users').update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})

    if result.modified_count == 0:
        return jsonify({'error': 'User not updated'}), 400
    
    user_dict.pop('password', None)
    user_dict['_id'] = str(user_id)
    return jsonify(user_dict), 200

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id: str) -> Response:
    user = get_collection('users').find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    result = get_collection('users').delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not deleted'}), 400

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)