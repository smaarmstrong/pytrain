from flask import Blueprint, Flask

api_bp = Blueprint("api", __name__)

# routes on api_bp: /status, /double/<int:n>, /hits — see prompt.md


def create_app(config=None):
    ...
