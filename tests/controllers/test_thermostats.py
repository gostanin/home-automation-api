import json

import pytest

from unittest.mock import patch


@pytest.fixture()
def get_return_value():
    return {
        'creation_date': '2018-20-20',
        'id': 1,
        'name': 'Mock thermostat',
        'temp': 64
    }


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_get_thermostats_200(get_model_thermostats, get_test_client, get_return_value):
    with get_test_client as app:
        get_model_thermostats().get_thermostats.return_value = [get_return_value]

        result = app.get('/api/v1/thermostats')
        data = json.loads(result.data)
        assert result.status_code == 200
        assert data[0]['id'] == 1
        assert data[0]['temp'] == 64
        assert data[0]['name']
        assert data[0]['creation_date']

        get_model_thermostats().get_thermostats.assert_called_once_with()


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_get_thermostats_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().get_thermostats.side_effect = Exception()

        result = app.get('/api/v1/thermostats')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']

        get_model_thermostats().get_thermostats.assert_called_once_with()


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_get_thermostat_200(get_model_thermostats, get_test_client, get_return_value):
    with get_test_client as app:
        get_model_thermostats().get_thermostat.return_value = get_return_value

        result = app.get('/api/v1/thermostats/1')
        data = json.loads(result.data)
        assert result.status_code == 200
        assert data['id'] == 1
        assert data['temp'] == 64
        assert data['name']
        assert data['creation_date']

        get_model_thermostats().get_thermostat.assert_called_once_with(1)


def test_get_thermostat_400(get_test_client):
    with get_test_client as app:
        result = app.get('/api/v1/thermostats/0')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_get_thermostat_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().get_thermostat.side_effect = Exception()

        result = app.get('/api/v1/thermostats/1')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@pytest.mark.parametrize('request_body',
                         [
                             {'name': 'Test thermostat', 'temp': 100},
                             {'name': 'Test thermostat', 'temp': -100},
                             {'name': 'Test thermostat', 'temp': 0}
                         ])
@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_save_thermostat_204(get_model_thermostats, get_test_client, request_body):
    with get_test_client as app:
        result = app.post('/api/v1/thermostats', json=request_body)
        assert result.status_code == 204

        name = request_body['name']
        temp = request_body['temp']
        get_model_thermostats().save_thermostat.assert_called_once_with(name, temp)


@pytest.mark.parametrize('request_body',
                         [
                             None,
                             {'name': '', 'temp': 64},
                             {'name': 'Test thermostat', 'temp': None},
                             {'name': 'Test thermostat', 'temp': -301},
                             {'name': 'Test thermostat', 'temp': 301}
                         ])
def test_save_thermostat_400(get_test_client, request_body):
    with get_test_client as app:
        result = app.post('/api/v1/thermostats', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_save_thermostat_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().save_thermostat.side_effect = Exception()

        request_body = {'name': 'Test thermostat', 'temp': 64}
        result = app.post('/api/v1/thermostats', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_remove_thermostat_204(get_model_thermostats, get_test_client):
    with get_test_client as app:
        result = app.delete('/api/v1/thermostats/1')
        assert result.status_code == 204

        get_model_thermostats().delete_thermostat.assert_called_once_with(1)


def test_remove_thermostat_400(get_test_client):
    with get_test_client as app:
        result = app.delete('/api/v1/thermostats/0')
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_remove_thermostat_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().delete_thermostat.side_effect = Exception()

        result = app.delete('/api/v1/thermostats/1')
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_update_temp_204(get_model_thermostats, get_test_client):
    with get_test_client as app:
        request_body = {'temp': 64}
        result = app.put('/api/v1/thermostats/1/temp', json=request_body)
        assert result.status_code == 204

        get_model_thermostats().update_temp.assert_called_once_with(1, request_body['temp'])


@pytest.mark.parametrize('request_dict',
                         [
                             {'id': 1, 'request_body': None},
                             {'id': 0, 'request_body': {'temp': 64}},
                             {'id': 1, 'request_body': {'temp': None}},
                             {'id': 1, 'request_body': {'temp': -301}},
                             {'id': 1, 'request_body': {'temp': 301}}
                         ])
def test_update_temp_400(get_test_client, request_dict):
    with get_test_client as app:
        id = request_dict['id']
        request_body = request_dict['request_body']
        result = app.put(f'/api/v1/thermostats/{id}/temp', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_update_temp_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().update_temp.side_effect = Exception()

        request_body = {'temp': 64}
        result = app.put('/api/v1/thermostats/1/temp', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_update_name_204(get_model_thermostats, get_test_client):
    with get_test_client as app:
        request_body = {'name': 'Test change name'}
        result = app.put('/api/v1/thermostats/1/name', json=request_body)
        assert result.status_code == 204

        get_model_thermostats().update_name.assert_called_once_with(1, request_body['name'])


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
        result = app.put(f'/api/v1/thermostats/{id}/name', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 400
        assert data['message']


@patch('home_automation.controllers.thermostats.get_model_thermostats')
def test_update_name_500(get_model_thermostats, get_test_client):
    with get_test_client as app:
        get_model_thermostats().update_name.side_effect = Exception()

        request_body = {'name': 'Test change name'}
        result = app.put('/api/v1/thermostats/1/name', json=request_body)
        data = json.loads(result.data)
        assert result.status_code == 500
        assert data['message']
