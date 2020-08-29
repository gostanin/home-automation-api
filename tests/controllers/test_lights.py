import json

import pytest

from unittest.mock import patch


@pytest.fixture()
def get_return_value():
    return {
        'creation_date': '2018-20-20',
        'id': 1,
        'name': 'Mock light',
        'status': 0
    }


@patch('home_automation.controllers.lights.get_model_lights')
def test_get_lights_200(get_model_lights, get_test_client, get_return_value):
    with get_test_client as app:
        get_lights_return = [get_return_value]

        get_model_lights().get_lights.return_value = get_lights_return

        result = app.get('/api/v1/lights')
        data = json.loads(result.data)
        assert result.status_code == 200
        assert data[0]['id'] == 1
        assert data[0]['status'] == 0
        assert data[0]['name']
        assert data[0]['creation_date']

        get_model_lights().get_lights.assert_called_once_with()


@patch('home_automation.controllers.lights.get_model_lights')
def test_get_lights_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().get_lights.side_effect = Exception()

        result = app.get('/api/v1/lights')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']

        get_model_lights().get_lights.assert_called_once_with()


@patch('home_automation.controllers.lights.get_model_lights')
def test_get_light_200(get_model_lights, get_test_client, get_return_value):
    with get_test_client as app:
        get_model_lights().get_light.return_value = get_return_value

        result = app.get('/api/v1/lights/1')
        data = json.loads(result.data)
        assert result.status_code == 200
        assert data['id'] == 1
        assert data['status'] == 0
        assert data['name']
        assert data['creation_date']

        get_model_lights().get_light.assert_called_once_with(1)


def test_get_light_400(get_test_client):
    with get_test_client as app:
        result = app.get('/api/v1/lights/0')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_get_light_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().get_light.side_effect = Exception()

        result = app.get('/api/v1/lights/1')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']

        get_model_lights().get_light.assert_called_once_with(1)


@pytest.mark.parametrize('request_body',
                         [
                             {'name': 'Test light'},
                             {'name': 'Test light', 'status': 1},
                             {'name': 'Test light', 'status': 0}
                         ])
@patch('home_automation.controllers.lights.get_model_lights')
def test_save_light_204(get_model_lights, get_test_client, request_body):
    with get_test_client as app:
        result = app.post('/api/v1/lights', json=request_body)
        assert result.status_code == 204

        name = request_body['name']
        status = 0 if 'status' not in request_body else request_body['status']
        get_model_lights().save_light.assert_called_once_with(name, status)


@pytest.mark.parametrize('request_body',
                         [
                             None,
                             {'name': ''},
                             {'name': 'Test light', 'status': 2},
                             {'name': 'Test light', 'status': -1}
                         ])
def test_save_light_400(get_test_client, request_body):
    with get_test_client as app:
        result = app.post('/api/v1/lights', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_save_light_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().save_light.side_effect = Exception()

        request_body = {'name': 'Test light'}
        result = app.post('/api/v1/lights', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_remove_light_204(get_model_lights, get_test_client):
    with get_test_client as app:
        result = app.delete('/api/v1/lights/1')
        assert result.status_code == 204

        get_model_lights().delete_light.assert_called_once_with(1)


def test_remove_light_400(get_test_client):
    with get_test_client as app:
        result = app.delete('/api/v1/lights/0')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_remove_light_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().delete_light.side_effect = Exception()

        result = app.delete('/api/v1/lights/1')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_on_light_204(get_model_lights, get_test_client):
    with get_test_client as app:
        result = app.put('/api/v1/lights/1/on')
        assert result.status_code == 204

        get_model_lights().update_status.assert_called_once_with(1, 1)


def test_on_lights_400(get_test_client):
    with get_test_client as app:
        result = app.put('/api/v1/lights/0/on')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_on_lights_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().update_status.side_effect = Exception()

        result = app.put('/api/v1/lights/1/on')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_off_light_204(get_model_lights, get_test_client):
    with get_test_client as app:
        result = app.put('/api/v1/lights/1/off')
        assert result.status_code == 204

        get_model_lights().update_status.assert_called_once_with(1, 0)


def test_off_lights_400(get_test_client):
    with get_test_client as app:
        result = app.put('/api/v1/lights/0/off')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_ff_lights_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().update_status.side_effect = Exception()

        result = app.put('/api/v1/lights/1/off')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_update_name_204(get_model_lights, get_test_client):
    with get_test_client as app:
        request_body = {'name': 'Test change name'}
        result = app.put('/api/v1/lights/1/name', json=request_body)
        assert result.status_code == 204

        get_model_lights().update_name.assert_called_once_with(1, request_body['name'])


@pytest.mark.parametrize('request_dict',
                         [
                             {'id': 1, 'request_body': None},
                             {'id': 0, 'request_body': {'name': 'Test change name'}},
                             {'id': 1, 'request_body': {'name': ''}}
                         ])
def test_update_name_400(get_test_client, request_dict):
    with get_test_client as app:
        id = request_dict['id']
        request_body = request_dict['request_body']
        result = app.put(f'/api/v1/lights/{id}/name', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.lights.get_model_lights')
def test_update_name_500(get_model_lights, get_test_client):
    with get_test_client as app:
        get_model_lights().update_name.side_effect = Exception()

        request_body = {'name': 'Test change name'}
        result = app.put('/api/v1/lights/1/name', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']
