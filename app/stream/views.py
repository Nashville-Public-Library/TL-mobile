from flask import make_response, redirect

from app import app
from app.stream.icecast import Icecast

@app.route('/stream', methods=['POST'])
def hmm():
    return "these aren't the droids you're looking for"

@app.route('/stream/status', methods=['POST'])
def now_playing():
    response = make_response(Icecast().now_playing)
    response.headers['customHeader'] = 'Darth Vader'
    response.status_code = 200
    response.content_type = 'application/json'
    response.access_control_allow_origin = '*'
    return response

@app.route('/stream/livestream.mp3')
def livestream_live():
    return redirect('https://npl.streamguys1.com/live')

@app.route('/stream/wpln.mp3')
def livestream_wpln():
    return redirect('https://npl.streamguys1.com/wpln')

@app.route('/stream/fallback.mp3')
def livestream_fallback():
    return redirect('https://npl.streamguys1.com/NPL-Fallback-for-WPLN-mount')