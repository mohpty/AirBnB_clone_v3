#!/usr/bin/python3
"""status class"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def list_states():
    """Retrieves a list of all State objects """
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves State objects"""
    state = storage.all("State").values()
    objs = [obj.to_dict() for obj in state if obj.id == state_id]
    if objs is None:
        abort(404)
    return jsonify(objs.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes State objects"""
    state = storage.all("State").values()
    objs = [obj.to_dict() for obj in state if obj.id == state_id]
    if objs == []:
        abort(404)
    objs.remove(objs[0])
    for obj in states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create state"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dic())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a state"""
    state = storage.all("State").values()
    objs = [obj.to_dict() for obj in state if obj.id == state_id]
    if objs == []:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    objs[0]['name'] = request.json['name']
    for obj in state:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(objs[0]), 200
