from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "dev-secret"

PASSWORD = "open-sesame"


@app.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    password = body.get("password")
    if not username or password != PASSWORD:
        session.pop("user", None)
        return jsonify({"error": "invalid credentials"}), 401
    session["user"] = username
    return jsonify({"user": username})


@app.get("/whoami")
def whoami():
    user = session.get("user")
    if user is None:
        return jsonify({"error": "not logged in"}), 401
    return jsonify({"user": user})


@app.post("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"user": None})


@app.get("/visits")
def visits():
    session["visits"] = session.get("visits", 0) + 1
    return jsonify({"visits": session["visits"]})
