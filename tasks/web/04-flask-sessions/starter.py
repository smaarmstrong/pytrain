from flask import Flask, session

app = Flask(__name__)
app.secret_key = "dev-secret"  # required for sessions

# POST /login, GET /whoami, POST /logout, GET /visits — see prompt.md
