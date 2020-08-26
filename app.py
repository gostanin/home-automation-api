from home_automation.app_factory import create_app
# from home_automation.database.database import main

if __name__ == "__main__":
    app = create_app()
    app.run(port=app.config['PORT'])
