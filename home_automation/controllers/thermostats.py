import logging

from flask import Blueprint, request, jsonify

from home_automation.model.model_factory import get_model_thermostats

thermostats = Blueprint('thermostats', __name__)

logger = logging.getLogger(__name__)


@thermostats.route('/', methods=['GET'], strict_slashes=False)
def get_thermostats():
    """Returns list of all thermostats
    All thermostats registered with home automation system
    ---
    tags: [Thermostats]
    definitions:
        Thermostat:
            type: object
            properties:
                creation_date:
                    type: string
                id:
                    type: integer
                name:
                    type: string
                temp:
                    type: integer
        Bad request:
            type: object
            properties:
                message:
                    type: string
        Error:
            type: object
            properties:
                message:
                    type: string
    responses:
        200:
            description: A list of thermostats
            schema:
                $ref: '#/definitions/Thermostat'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    res = None
    try:
        res = get_model_thermostats().get_thermostats()
        logger.info('[GET] Thermostats all')
    except Exception:
        logger.exception('[GET] Thermostats all exception')
        return jsonify(message='Unexpected error occured while getting thermostats'), 500

    return jsonify(res), 200


@thermostats.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_thermostat(id):
    """Returns thermostat by id
    ---
    tags: [Thermostats]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
    responses:
        200:
            description: Thermostat returned by id
            schema:
                $ref: '#/definitions/Thermostat'
        400:
            description: id less than 1
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    if id < 1:
        logger.warning(f'[GET] Incorrect thermostat id: {id}')
        return jsonify(message='Thermostats id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_thermostats().get_thermostat(id)
        logger.info(f'[GET] Thermostat id: {id}')
    except Exception:
        logger.exception(f'[GET] Thermostats id: {id} exception')
        return jsonify(message='Unexpected error occured while getting thermostat'), 500

    return jsonify(res), 200


@thermostats.route('/', methods=['POST'], strict_slashes=False)
def save_thermostat():
    """Creates thermostat
    Adds thermostat in home automation system
    ---
    tags: [Thermostats]
    parameters:
      - name: name
        in: query
        type: string
        required: true
      - name: temp
        minimum: -300
        maximum: 300
        in: query
        type: integer
        required: true
    responses:
        204:
            description: Thermostat created
        400:
            description: Data missing - empty query or [name] or [temp]
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    data = request.get_json()

    if not data:
        logger.warning('[POST] Thermostats request body is empty')
        return jsonify(message='Thermostats data is missing'), 400

    name = data.get('name')
    temp = data.get('temp')

    if not name:
        logger.warning('[POST] Thermostats request body has no [name]')
        return jsonify(message='Thermostats data is missing parameter: name'), 400
    if not temp and temp != 0:
        logger.warning('[POST] Thermostats request body has no [temp]')
        return jsonify(message='Thermostats data is missing parameter: temp'), 400
    if temp > 300 or temp < -300:
        logger.warning('[POST] Thermostats [temp] is out of range[-300, 300]')
        return jsonify(message='Thermostats data is out of range[-300, 300] parameter: temp'), 400

    try:
        get_model_thermostats().save_thermostat(name, temp)
        logger.info(f'[POST] Thermostat added name: {name}, temp: {temp}')
    except Exception:
        logger.exception('[POST] Thermostats exception')
        return jsonify(message='Unexpected error occured while saving thermostat'), 500

    return '', 204


@thermostats.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_thermostat(id):
    """Deletes thermostat
    Removes thermostat from home automation system
    ---
    tags: [Thermostats]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
    responses:
        204:
            description: Thermostat deleted
        400:
            description: id less than 1
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    if id < 1:
        logger.warning(f'[DELETE] Incorrect thermostat id: {id}')
        return jsonify(message='Thermostats id must be strictly greater than 0'), 400

    try:
        get_model_thermostats().delete_thermostat(id)
        logger.info(f'[DELETE] Thermostat id: {id}')
    except Exception:
        logger.exception('[DELETE] Thermostats exception')
        return jsonify(message='Unexpected error occured while removing thermostat'), 500

    return '', 204


@thermostats.route('/<int:id>/temp', methods=['PUT'], strict_slashes=False)
def update_temp(id):
    """Updates thermostat temperature
    ---
    tags: [Thermostats]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
      - name: temp
        in: query
        type: integer
        required: true
    responses:
        204:
            description: Thermostat temperature updated
        400:
            description: id less than 1 or data missing - [temp]
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    data = request.get_json()

    if not data:
        logger.warning(f'[PUT] Thermostats request body for update temp is empty for id: {id}')
        return jsonify(message='Thermostats data is missing'), 400
    if id < 1:
        logger.warning(f'[PUT] Incorrect thermostat id: {id}')
        return jsonify(message='Thermostats id must be strictly greater than 0'), 400

    temp = data.get('temp')

    if not temp:
        logger.warning(f'[PUT] Thermostats request body has no [temp] for id: {id}')
        return jsonify(message='Thermostats data is missing parameter: temp'), 400
    if temp > 300 or temp < -300:
        logger.warning('[PUT] Thermostats [temp] is out of range[-300, 300]')
        return jsonify(message='Thermostats data is out of range[-300, 300] parameter: temp'), 400

    try:
        get_model_thermostats().update_temp(id, temp)
        logger.info(f'[PUT] Thermostat has been updated id: {id}, temp: {temp}')
    except Exception:
        logger.exception('[PUT] Thermostats exception')
        return jsonify(message='Unexpected error occured while updating thermostat'), 500

    return '', 204


@thermostats.route('/<int:id>/name', methods=['PUT'], strict_slashes=False)
def update_name(id):
    """Updates thermostat name
    ---
    tags: [Thermostats]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
      - name: name
        in: query
        type: string
        required: true
    responses:
        204:
            description: Thermostat name updated
        400:
            description: id less than 1 or data missing - [name]
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    data = request.get_json()

    if not data:
        logger.warning(f'[PUT] Thermostats request body for update name is empty for id: {id}')
        return jsonify(message='Thermostats data is missing'), 400
    if id < 1:
        logger.warning(f'[PUT] Incorrect thermostat id: {id}')
        return jsonify(message='Thermostats id must be strictly greater than 0'), 400

    name = data.get('name')

    if not name:
        logger.warning(f'[PUT] Thermostats request body has no [name] for id: {id}')
        return jsonify(message='Thermostats data is missing parameter: name'), 400

    try:
        get_model_thermostats().update_name(id, name)
        logger.info(f'[PUT] Thermostat has been updated id: {id}, temp: {name}')
    except Exception:
        logger.exception('[PUT] Thermostats exception')
        return jsonify(message='Unexpected error occured while updating thermostat'), 500

    return '', 204
