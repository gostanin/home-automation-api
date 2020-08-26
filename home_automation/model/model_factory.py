from home_automation.model.model_lights import ModelLights
from home_automation.model.model_thermostats import ModelThermostats


def get_model_lights():
    return ModelLights()


def get_model_thermostats():
    return ModelThermostats()
