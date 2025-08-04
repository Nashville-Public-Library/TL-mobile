from datetime import datetime, timezone

from flask import render_template, request, jsonify

from app import app
from app.status.ping import ping, Icecast
from app.auth import require_auth
from app.sql import SQL

@app.route('/status', methods=['GET'])
@require_auth
def status():
        return render_template('status.html')

@app.route('/status/ping', methods=['POST'])
@require_auth
def ping_ip():
    ping_list = {
        "icecast": "npl.streamguys1.com",
        "wpln": "12.247.152.50",
        "SGmetadata": "204.93.152.147",
        "metro": "170.190.43.1",
        "npl": "library.nashville.org",
        "pod": "assets.library.nashville.org",
        "vic": "www.volgistics.com",
        "zeno": "fluoz.zeno.fm"
        }
    host: dict = request.get_json()
    host = host.get("host")
    host = ping_list.get(host)
    pingable = ping(host=host)
    return {"result": pingable}

@app.route('/status/stream', methods=['POST'])
@require_auth
def stream():
    icecast = Icecast()
    return {
         'mounts': icecast.mounts, 
         'listeners': icecast.listeners, 
         'serverStart': icecast.server_start, 
         'outgoing_kbitrate': icecast.outgoing_kbitrate,
         'sources': icecast.sources
         }

@app.route('/status/mounts', methods=['POST'])
@require_auth
def mount_list():
     icecast = Icecast()
     return {'mountList': icecast.mount_list}   

@app.route('/status/useragent', methods=['POST'])
@require_auth
def user_agent():
     icecast = Icecast()
     mount:dict = request.get_json()
     mount = mount.get("mount")
     return {'userAgent': icecast.user_agent_ip(mount=mount)}

@app.route("/status/heartbeat", methods=["POST"])
@require_auth
def heartbeat_post():
     response: dict = request.get_json()
     hostname = response.get("hostname")
     ip_address = response.get("ip_address")
     last_seen = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
     SQL().write_heartbeat(hostname=hostname, ip_address=ip_address, last_seen=last_seen)
    
     return {"response": "success"}, 200

@app.route("/status/heartbeat/listdevices", methods=["POST"])
@require_auth
def heartbeart_devices():
     devices =  SQL().read_heartbeat()
     devices = jsonify(devices)
     print(devices)
     return devices
