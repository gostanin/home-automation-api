from flask import Blueprint, request, jsonify

from home_automation.model.model_factory import get_model_lights

lights = Blueprint('lights', __name__)


@lights.route('/', methods=['GET'], strict_slashes=False)
def get_lights():
    res = None
    try:
        res = get_model_lights().get_lights()
    except Exception as e:
        # logging
        return jsonify(f'Unexpected error occured while getting the lights {e}'), 500

    return jsonify(res), 200


@lights.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_light(id):
    if id < 1:
        return jsonify('Light\'s id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_lights().get_light(id)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the lights {e}'), 500

    return jsonify(res), 200


@lights.route('/', methods=['POST'], strict_slashes=False)
def save_light():
    data = request.get_json()

    if not data:
        return 'Light\'s data is missing', 400

    name = data.get('name')
    status = data.get('status')

    if not name:
        return 'Light\'s data is missing parameter: name', 400
    if not status:
        status = 0

    res = None
    try:
        res = get_model_lights().save_light(name, status)
    except Exception as e:
        # logging
        return jsonify(f'Unexpected error occured while getting the lights | {e}'), 500

    return jsonify(res), 201


@lights.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_light(id):
    if id < 1:
        return jsonify('Light\'s id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_lights().delete_light(id)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the lights | {e}'), 500

    return jsonify(res), 200


# TO-DO switch instead of on/off. Not doing it because of ALL ON/OFF operations
@lights.route('/<int:id>/on', methods=['PUT'], strict_slashes=False)
def on_light(id):
    if id < 1:
        return jsonify('Light\'s id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_lights().update_status(id, 1)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the lights | {e}'), 500

    return jsonify(res), 200


@lights.route('/<int:id>/off', methods=['PUT'], strict_slashes=False)
def off_light(id):
    if id < 1:
        return jsonify('Light\'s id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_lights().update_status(id, 0)
    except Exception as e:
        return jsonify(f'Unexpected error occured while getting the lights | {e}'), 500

    return jsonify(res), 200

# TO-DO turning all lights off and on. Not supporting on backend
