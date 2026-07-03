"""App factory — the grader does `from app import create_app` (via loader).

Register the blueprint from entries.py under /entries, add the GET /
health route, give each app its own entry store. See prompt.md.
"""


def create_app():
    raise NotImplementedError("see prompt.md")
