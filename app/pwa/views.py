from flask import render_template, make_response, request

from app import app
from app.pwa.pod import Podcast
from app.pwa.weather import get_weather

VERSION = "0.7.22"

@app.route('/', methods=['GET'])
def pwa():
    return app.send_static_file("pages/index.html")

@app.route('/version', methods=['POST'])
def version():
    return {"version": VERSION}

@app.route('/sw.js')
def serve_sw():
    response = make_response(render_template("sw.js", version=VERSION))
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route('/detect.js')
def serve_app_js():
    response = make_response(render_template("detect.js", version=VERSION))
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route('/podcasts/info/<podcast>', methods=['POST'])
def podcasts_info(podcast):
    try:
        pod = Podcast(show=podcast)
        pod = pod.to_client()

        return render_template("podcast-individual.html", pod=pod)  
    except:
        return "", 500
    
@app.route("/weather", methods=["POST"])
def weather():
    json:dict = request.get_json()
    station = json.get("station")
    weather = get_weather(station=station)

    return weather