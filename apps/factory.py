import logging
import os
import sys
from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from flask_mongoengine import MongoEngine

# mongo = PyMongo()


def create_app(config_type="config.Config"):
    "Main thread"
    # Create flask app object
    app = Flask(__name__)
    # Setting configuration for the project
    app.config.from_object(config_type)
    app.config["MONGODB_SETTINGS"] = {
        "host": os.getenv(
            "MONGO_URI", "mongodb://payroll_mongo:27017/payrolldb_2023"
        )
    }
    # Adding log level
    app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    app.logger.setLevel(logging.DEBUG)
    db = MongoEngine(app)
    # initialize mongo app
    # mongo.init_app(app)

    # Register blueprint
    from apps.payroll_service.controller import payroll

    app.register_blueprint(payroll)

    return app
