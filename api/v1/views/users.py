#!/usr/bin/python3
"""Users"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.user import User


@app_views.route("/users")
def user_index():
    users = storage.all(User).values()
    users_list = list(map(lambda user: user.to_dict(), users))
    return (json.dumps(users_list))


@app_views.route("/users/<user_id>")
def user_get(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            return json.dumps(user.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/users/<user_id>", methods=['DELETE'])
def user_delete(user_id):
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            user.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/users", methods=['POST'])
def user_post():
    try:
        data = request.get_json()
        if "email" not in data:
            return make_response(
                jsonify({'message': 'Missing email'}), 400)
        if "password" not in data:
            return make_response(
                jsonify({'message': 'Missing password'}), 400)
        user = User()
        user.email = data['email']
        user.password = data['password']
        storage.new(user)
        storage.save()
        return make_response(user.to_dict(), 201)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)


@app_views.route("/users/<user_id>", methods=['PUT'])
def user_update(user_id):
    try:
        data = request.get_json()
        users = storage.all(User).values()
        for user in users:
            if user.id == user_id:
                if "first_name" in data:
                    user.first_name = request.get_json()['first_name']
                if "last_name" in data:
                    user.last_name = request.get_json()['last_name']
                if "password" in data:
                    user.password = request.get_json()['password']
                storage.save()
                return make_response(user.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)
