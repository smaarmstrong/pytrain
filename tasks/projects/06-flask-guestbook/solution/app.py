"""App factory: fresh app + fresh in-memory store per call."""
from flask import Flask, jsonify

from entries import bp


def create_app():
    app = Flask(__name__)
    app.extensions["guestbook"] = {"entries": [], "next_id": 1}
    app.register_blueprint(bp, url_prefix="/entries")

    @app.get("/")
    def health():
        return jsonify({"status": "ok"})

    return app
