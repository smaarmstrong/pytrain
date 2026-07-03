from flask import Blueprint, Flask, current_app, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.get("/status")
def status():
    name = current_app.config.get("APP_NAME", "default")
    return jsonify({"status": "ok", "app_name": name})


@api_bp.get("/double/<int:n>")
def double(n):
    return jsonify({"result": 2 * n})


@api_bp.post("/hits")
def hits():
    current_app.config["HITS"] = current_app.config.get("HITS", 0) + 1
    return jsonify({"hits": current_app.config["HITS"]})


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    return app
