from fastapi import FastAPI

app = FastAPI()

# POST /users, GET /users, GET /users/{user_id}, DELETE /users/{user_id}
# — see prompt.md. Responses must never leak the stored password.
