import logging

from flask import Blueprint, request, jsonify

from home_automation.model.model_factory import get_model_thermostats

thermostats = Blueprint('thermostats', __name__)

logger = logging.getLogger(__name__)


@thermostats.route('/', methods=['GET'], strict_slashes=False)
def get_thermostats():
    res = None
    try:
        res = get_model_thermostats().get_thermostats()
        logger.info('[GET] Thermostats all')
    except Exception:
        logger.exception('[GET] Thermostats all exception')
        return jsonify('Unexpected error occured while getting thermostats'), 500

    return jsonify(res), 200


@thermostats.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_thermostat(id):
    if id < 1:
        logger.warning(f'[GET] Incorrect thermostat id: {id}')
        return jsonify('Thermostats id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_thermostats().get_thermostat(id)
        logger.info(f'[GET] Thermostat id: {id}')
    except Exception:
        logger.exception('[GET] Thermostats all exception')
        return jsonify('Unexpected error occured while getting thermostat'), 500

    return jsonify(res), 200


@thermostats.route('/', methods=['POST'], strict_slashes=False)
def save_thermostat():
    data = request.get_json()

    if not data:
        logger.warning('[POST] Thermostats request body is empty')
        return 'Thermostats data is missing', 400

    name = data.get('name')
    temp = data.get('temp')

    if not name:
        logger.warning('[POST] Thermostats request body has no [name]')
        return 'Thermostats data is missing parameter: name', 400
    if not temp:
        logger.warning('[POST] Thermostats request body has no [temp]')
        return 'Thermostats data is missing parameter: temp', 400

    res = None
    try:
        res = get_model_thermostats().save_thermostat(name, temp)
        logger.info(f'[POST] Thermostat added name: {name}, temp: {temp}')
    except Exception:
        logger.exception('[POST] Thermostats exception')
        return jsonify('Unexpected error occured while saving thermostat'), 500

    return jsonify(res), 201


@thermostats.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_thermostat(id):
    if id < 1:
        logger.warning(f'[DELETE] Incorrect thermostat id: {id}')
        return jsonify('Thermostats id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_thermostats().delete_thermostat(id)
        logger.info(f'[DELETE] Thermostat id: {id}')
    except Exception:
        logger.exception('[DELETE] Thermostats exception')
        return jsonify('Unexpected error occured while removing thermostat'), 500

    return jsonify(res), 200


@thermostats.route('/<int:id>', methods=['PUT'], strict_slashes=False)
def update_temp(id):
    data = request.get_json()

    if not data:
        logger.warning(f'[PUT] Thermostats request body is empty for id: {id}')
        return jsonify('Thermostats data is missing'), 400
    if id < 1:
        logger.warning(f'[PUT] Incorrect thermostat id: {id}')
        return jsonify('Thermostats id must be strictly greater than 0'), 400

    temp = data.get('temp')

    if not temp:
        logger.warning(f'[PUT] Thermostats request body has no [temp] for id: {id}')
        return jsonify('Thermostats data is missing parameter: temp'), 400

    res = None
    try:
        res = get_model_thermostats().update_temp(id, temp)
        logger.info(f'[PUT] Thermostat has been updated id: {id}, temp: {temp}')
    except Exception:
        logger.exception('[PUT] Thermostats exception')
        return jsonify('Unexpected error occured while updating thermostat'), 500

    return jsonify(res), 200
