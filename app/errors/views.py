from flask import redirect

from app import app

# do something to explicitly handle HTTP errors so we don't get some general nginx page

@app.errorhandler(400)
def bad_request(e):
    return "you're no good, you're no good", 400

@app.errorhandler(404)
def not_found(e):
    return redirect(location="/")

@app.errorhandler(405)
def not_allowed(e):
    return "you're no good, you're no good", 405

@app.errorhandler(500)
def handle_exception(e):
    return "SOMETHING BAD HAPPENED!", 500