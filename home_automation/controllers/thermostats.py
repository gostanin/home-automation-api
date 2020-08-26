from flask import Blueprint, request, jsonify

from home_automation.model.model_factory import get_model_thermostats

thermostats = Blueprint('thermostats', __name__)


@thermostats.route('/', methods=['GET'], strict_slashes=False)
def get_thermostats():
    res = None
    try:
        res = get_model_thermostats().get_thermostats()
    except Exception as e:
        print(e)

    return jsonify(res), 200


@thermostats.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_thermostat(id):
    if id < 1:
        return jsonify('Thermostats\' id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_thermostats().get_thermostat(id)
    except Exception as e:
        print(e)

    return jsonify(res), 200


@thermostats.route('/', methods=['POST'], strict_slashes=False)
def save_thermostat():
    data = request.get_json()

    if not data:
        return 'Thermostats\' data is missing', 400

    name = data.get('name')
    temp = data.get('temp')

    if not name:
        return 'Thermostats\' data is missing parameter: name', 400
    if not temp:
        return 'Thermostats\' data is missing parameter: temp', 400

    res = None
    try:
        res = get_model_thermostats().save_thermostat(name, temp)
    except Exception as e:
        # logging
        return jsonify(f'Unexpected error occured while getting the Thermostats | {e}'), 500

    return jsonify(res), 201


@thermostats.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_thermostat(id):
    if id < 1:
        return jsonify('Thermostats\' id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_thermostats().delete_thermostat(id)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the Thermostats | {e}'), 500

    return jsonify(res), 200


@thermostats.route('/<int:id>', methods=['PUT'], strict_slashes=False)
def update_temp(id):
    data = request.get_json()

    if not data:
        return jsonify('Thermostats\'s no data'), 400
    if id < 1:
        return jsonify('Thermostats\'s id must be strictly greater than 0'), 400

    temp = data.get('temp')

    if not temp:
        return jsonify('Thermostats\'s temp must be'), 400

    res = None
    try:
        res = get_model_thermostats().update_temp(id, temp)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the Thermostats | {e}'), 500

    return jsonify(res), 200
