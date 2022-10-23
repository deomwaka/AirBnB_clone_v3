#!/usr/bin/python3
"""handles states"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST', 'GET'])
def state_cities(state_id):
    """get cities depending on state"""
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            cities = state.cities
            list1 = []
            for city in cities:
                list1.append(city.to_dict())
            return jsonify(list1)
    if request.method == 'POST':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                return "Not a JSON", 400
            if "name" not in data:
                return "Missing name", 400
            data.update({'state_id': state_id})
            new_city = City(**data)
            return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['POST', 'GET', 'DELETE'])
def cities(city_id):
    """get cities on id"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            return jsonify(city.to_dict())
    if request.method == 'DELETE':
        obj = storage.get(City, city_id)
        if obj is None:
            abort(404)
        else:
            storage.delete(obj)
            storage.save()
            return {}, 200
    if request.method == 'PUT':
        obj = storage.get(City, city_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                return "Not a JSON", 400

            for k, v in data.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(obj, k, v)
            obj.save()
            storage.reload()
            return jsonify(obj.to_dict()), 200
