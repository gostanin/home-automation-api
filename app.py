import logging

from home_automation.app_factory import create_app
from home_automation.database.database import create_database


logging.basicConfig(level=logging.INFO,
                    filename='home_automation.log',
                    datefmt='%Y-%m-%S %H:%M:%S',
                    format='%(levelname)s - %(asctime)s / %(message)s / %(name)s / line: %(lineno)d'
                    )

logger = logging.getLogger('werkzeug')
logger.disabled = True

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("--------Application start-------")
    create_database()
    app = create_app()
    app.run(port=app.config['PORT'])
    logger.info("--------Application stop--------")
