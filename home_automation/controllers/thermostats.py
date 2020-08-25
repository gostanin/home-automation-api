from flask import Blueprint, request, jsonify

thermostats = Blueprint('thermostats', __name__)


@thermostats.route('/', methods=['GET'], strict_slashes=False)
def get_thermostats():
    pass


@thermostats.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_thermostat(id):
    pass


@thermostats.route('/', methods=['POST'], strict_slashes=False)
def save_thermostat():
    pass


@thermostats.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_thermostat(id):
    pass


@thermostats.route('/<int:id>', methods=['PUT'], strict_slashes=False)
def update_thermostat():
    pass
