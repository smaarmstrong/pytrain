"""Guestbook blueprint: JSON responses, form-or-JSON submissions."""
from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("entries", __name__)


def _store():
    return current_app.extensions["guestbook"]


@bp.get("/")
def list_entries():
    return jsonify(_store()["entries"])


@bp.post("/")
def add_entry():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form
    name = (data.get("name") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not message:
        return jsonify({"error": "name and message are required"}), 400
    store = _store()
    entry = {"id": store["next_id"], "name": name, "message": message}
    store["next_id"] += 1
    store["entries"].append(entry)
    return jsonify(entry), 201


@bp.get("/<int:entry_id>")
def get_entry(entry_id):
    for entry in _store()["entries"]:
        if entry["id"] == entry_id:
            return jsonify(entry)
    return jsonify({"error": "not found"}), 404
