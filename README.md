## Installation

Application served on _localhost:8000/api/v1/_

Swagger documentation for API endpoints on _localhost:8000/apidocs/_

​#### Docker:

​		Run `make docker_up`

​		Tests `make docker_test`

​		Stop `make docker_stop`

​		Tear down container `make docker_down`

​#### Regular installation:

​		Virtual environment `python -m venv .venv`

​		Start venv `source .venv/bin/activate`

​		Dependencies `pip3 install -r requirements.txt`

​		Tests run `pytest`

​		Run `python app.py`
