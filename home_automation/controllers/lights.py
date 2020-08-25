from flask import Blueprint, request, jsonify

lights = Blueprint('lights', __name__)


@lights.route('/', methods=['GET'], strict_slashes=False)
def get_lights():
    pass


@lights.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_light(id):
    pass


@lights.route('/', methods=['POST'], strict_slashes=False)
def save_light():
    pass


@lights.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_light(id):
    pass


# TO-DO switch instead of on/off
@lights.route('/<int:id>/on', methods=['PUT'], strict_slashes=False)
def on_light(id):
    pass


@lights.route('/<int:id/off', methods=['PUT'], strict_slashes=False)
def off_light(id):
    pass


# TO-DO turning all lights off and on
