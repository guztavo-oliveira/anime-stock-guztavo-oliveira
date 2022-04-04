from flask import Flask, Blueprint
from dotenv import load_dotenv
from app import routes

load_dotenv()


def create_app():

    app = Flask(__name__)

    routes.init_app(app)

    return app
