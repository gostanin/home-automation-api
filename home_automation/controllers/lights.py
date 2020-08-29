import logging

from flask import Blueprint, request, jsonify

from home_automation.model.model_factory import get_model_lights

lights = Blueprint('lights', __name__)

logger = logging.getLogger(__name__)


@lights.route('/', methods=['GET'], strict_slashes=False)
def get_lights():
    """Returns list of all lights
    All lights registered with home automation system
    ---
    tags: [Lights]
    definitions:
        Light:
            type: object
            properties:
                creation_date:
                    type: string
                id:
                    type: integer
                name:
                    type: string
                status:
                    type: integer
    responses:
        200:
            description: A list of lights
            schema:
                $ref: '#/definitions/Light'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    res = None
    try:
        res = get_model_lights().get_lights()
        logger.info('[GET] Lights all')
    except Exception:
        logger.exception('[GET] Lights all exception')
        return jsonify(message='Unexpected error occured while getting lights'), 500

    return jsonify(res), 200


@lights.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_light(id):
    """Returns light by id
    ---
    tags: [Lights]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
    responses:
        200:
            description: Light returned by id
            schema:
                $ref: '#/definitions/Light'
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
        logger.warning(f'[GET] Incorrect lights id: {id}')
        return jsonify(message='Light id must be strictly greater than 0'), 400

    res = None
    try:
        res = get_model_lights().get_light(id)
        logger.info(f'[GET] Light id: {id}')
    except Exception:
        logger.exception(f'[GET] Light id: {id} exception')
        return jsonify(message='Unexpected error occured while getting light'), 500

    return jsonify(res), 200


@lights.route('/', methods=['POST'], strict_slashes=False)
def save_light():
    """Creates light
    Adds light in home automation system
    ---
    tags: [Lights]
    parameters:
      - name: Light to create
        in: body
        schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
              status:
                type: integer
                default: 0
                enum: [0, 1]
    responses:
        204:
            description: Light created
        400:
            description: Data missing - empty body or [name]
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    data = request.get_json()

    if not data:
        logger.warning('[POST] Lights request body is empty')
        return jsonify(message='Light data is missing'), 400

    name = data.get('name')
    status = data.get('status')

    if not name:
        logger.warning('[POST] Lights request body has no [name]')
        return jsonify(message='Light data is missing parameter: name'), 400
    if not status:
        logger.warning('[POST] Lights request body has no [status]. Status set to default(0)')
        status = 0
    if status > 1 or status < 0:
        logger.warning('[POST] Lights status must be either 0 or 1')
        return jsonify(message='Light data is out of range[0, 1] parameter: name'), 400

    try:
        get_model_lights().save_light(name, status)
        logger.info(f'[POST] Lights added name: {name}, status: {status}')
    except Exception:
        logger.exception('[POST] Lights exception')
        return jsonify(message='Unexpected error occured while saving light'), 500

    return '', 204


@lights.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def remove_light(id):
    """Deletes light
    Removes light from home automation system
    ---
    tags: [Lights]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
    responses:
        204:
            description: Light deleted
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
        logger.warning(f'[DELETE] Incorrect light id: {id}')
        return jsonify(message='Light id must be strictly greater than 0'), 400

    try:
        get_model_lights().delete_light(id)
        logger.info(f'[DELETE] Light id: {id}')
    except Exception:
        logger.exception('[DELETE] Lights exception')
        return jsonify(message='Unexpected error occured while deleting light'), 500

    return '', 204


# TO-DO switch instead of on/off. Not doing it because of ALL ON/OFF operations
@lights.route('/<int:id>/on', methods=['PUT'], strict_slashes=False)
def on_light(id):
    """Turns light on
    ---
    tags: [Lights]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
    responses:
        204:
            description: Light has been tuned on
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
        logger.warning(f'[PUT] Incorrect light id: {id} to turn on')
        return jsonify(message='Light id must be strictly greater than 0'), 400

    try:
        get_model_lights().update_status(id, 1)
        logger.info(f'[PUT] Light has been turned on id: {id}')
    except Exception:
        logger.exception('[PUT] Light on exception')
        return jsonify(message='Unexpected error occured while turnning light on'), 500

    return '', 204


@lights.route('/<int:id>/off', methods=['PUT'], strict_slashes=False)
def off_light(id):
    """Turns light off
    ---
    tags: [Lights]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1`
        required: true
    responses:
        204:
            description: Light has been tuned off
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
        logger.warning(f'[PUT] Incorrect light id: {id} to turn off')
        return jsonify(message='Light id must be strictly greater than 0'), 400

    try:
        get_model_lights().update_status(id, 0)
        logger.info(f'[PUT] Light has ben turned off id: {id}')
    except Exception:
        logger.exception('[PUT] Light off exception')
        return jsonify(message='Unexpected error occured while turning light off'), 500

    return '', 204


@lights.route('/<int:id>/name', methods=['PUT'], strict_slashes=False)
def update_name(id):
    """Updates light name
    ---
    tags: [Lights]
    parameters:
      - name: id
        in: path
        type: integer
        minimum: 1
        required: true
      - name: Light name to update
        in: body
        schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
    responses:
        204:
            description: Name was updated
        400:
            description: id less than 1 or data body is missing
            schema:
                $ref: '#/definitions/Bad request'
        500:
            description: Internal error
            schema:
                $ref: '#/definitions/Error'
    """
    data = request.get_json()

    if not data:
        logger.warning('[PUT] Lights request body for update name is empty')
        return jsonify(message='Light data is missing'), 400
    if id < 1:
        logger.warning(f'[PUT] Incorrect light id: {id} for update name')
        return jsonify(message='Light id must be strictly greater than 0'), 400

    name = data.get('name')

    if not name:
        logger.warning('[PUT] Lights request body has no [name]')
        return jsonify(message='Light data is missing parameter: name'), 400

    try:
        get_model_lights().update_name(id, name)
        logger.info(f'[PUT] Light name has been updated for id: {id}')
    except Exception:
        logger.exception('[PUT] Light update name exception')
        return jsonify(message='Unexpected error occured while updating name'), 500

    return '', 204
