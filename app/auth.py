from functools import wraps

from flask import Response, request

from app.ev import EV

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'whoops, you must supply credentials', 
    401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def require_auth_if_outside_metro(mah):
    """A decorator function that wraps other routes to check authentication"""
    @wraps(mah)
    def decorated():
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')
        if ip[0] in ('170.190.43.1', '127.0.0.1'):
             return mah()
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return mah()
    return decorated

def require_auth(mah):
    @wraps(mah)
    def decorated():
        auth = request.authorization
        if not auth or not check_auth(username=auth.username, password=auth.password):
            return authenticate()
        return mah()
    return decorated

def check_auth(username: str, password: str) -> bool:
    """This function is called to check if a username /
    password combination is valid.
    """
    return username.lower() == 'admin' and password.lower() == EV().BF_pass