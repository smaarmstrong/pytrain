from flask import Flask, abort, jsonify, request

app = Flask(__name__)

items: dict[int, dict] = {}
next_id = 1


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not found", "path": request.path}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "bad request", "detail": e.description}), 400


@app.post("/items")
def create_item():
    global next_id
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        body = {}
    name = body.get("name")
    if not isinstance(name, str) or not name:
        abort(400, description="name is required")
    price = body.get("price")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        abort(400, description="price must be a non-negative number")
    item = {"id": next_id, "name": name, "price": price}
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201


@app.get("/items/<int:item_id>")
def get_item(item_id):
    if item_id not in items:
        abort(404)
    return jsonify(items[item_id])
