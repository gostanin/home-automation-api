from flask import Flask
from flask_cors import CORS

from home_automation.controllers.lights import lights
from home_automation.controllers.thermostats import thermostats


def create_app():
    app = Flask(__name__)
    app.config.from_object('home_automation.settings')
    CORS(app, resources={r'/*': {'origins': app.config['ALLOWED_CORS_ORIGINS']}})
    app.register_blueprint(lights, url_prefix='/api/v1/lights')
    app.register_blueprint(thermostats, url_prefix='/api/v1/thermostats')

    return app
