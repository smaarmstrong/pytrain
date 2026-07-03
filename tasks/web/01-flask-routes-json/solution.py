from flask import Flask, jsonify, request

app = Flask(__name__)

notes: list[dict] = []
next_id = 1


@app.get("/ping")
def ping():
    return jsonify({"pong": True})


@app.get("/greet/<name>")
def greet(name):
    greeting = request.args.get("greeting", "Hello")
    return jsonify({"message": f"{greeting}, {name}!"})


@app.post("/notes")
def create_note():
    global next_id
    body = request.get_json()
    note = {"id": next_id, "text": body["text"]}
    notes.append(note)
    next_id += 1
    return jsonify(note), 201


@app.get("/notes")
def list_notes():
    contains = request.args.get("contains")
    out = notes
    if contains is not None:
        out = [n for n in notes if contains in n["text"]]
    return jsonify(out)


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    for n in notes:
        if n["id"] == note_id:
            return jsonify(n)
    return jsonify({"error": "not found"}), 404
