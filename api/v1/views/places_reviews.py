#!/usr/bin/python3
"""Reviews"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews')
def review_index(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            return json.dumps(list(map(lambda review: review.to_dict(),
                              place.reviews)))
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/reviews/<review_id>')
def review_get(review_id):
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            return json.dumps(review.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            review.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/places/<place_id>/reviews', methods=["POST"])
def review_post(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            try:
                data = request.get_json()
                if 'user_id' not in data:
                    return make_response(jsonify({'message': 'Missing user_id'}),
                                         400)
                if 'text' not in data:
                    return make_response(jsonify({'message': 'Missing text'}),
                                         400)                         
                review = Review()
                review.user_id = data['user_id']
                review.text = data['text']
                review.place_id = place_id
                storage.new(review)
                storage.save()
                return make_response(review.to_dict(), 201)
            except Exception:
                return make_response(jsonify({'message': 'Not a JSON'}), 400)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    try:
        data = request.get_json()
        reviews = storage.all(Review).values()
        for review in reviews:
            if review.id == review_id:
                if "text" in data:
                    review.text = request.get_json()['text']
                storage.save()
                return make_response(review.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)
