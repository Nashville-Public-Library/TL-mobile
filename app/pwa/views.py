import time

from flask import render_template, make_response
import requests

from app import app
from app.pwa.pod import Podcast

VERSION = "0.6.13"

weather_cache = {"data": None, "timestamp": 0}

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

@app.route('/app.js')
def serve_app_js():
    response = make_response(render_template("app.js", version=VERSION))
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route('/podcasts', methods=['POST'])
def podcasts():
    shows = {"AARP Report": "aarp", "Able Living": "able", "Around the World": "aroundworld", "Atlantic": "atlantic", "Book Page": "bookpage", 
             "Checklist": "checklist", "Hourly Weather Forecast": "cirrus", "Community News": "community", "Consumer Reports": "consumer", 
             "Diabetic News": "diabetes", "Discover": "discover", "Economist": "economist", "Entertainment Weekly": "entertainment", 
             "Eyes on Success": "eyes", "Fortune": "fortune", "Historical View": "historical", "An Hour of Short Stories": "hourshortstories", 
             "Independent Living": "independent", "Nashville Ledger": "ledger", "LGBTQ News & Culture": "lgbt", "Men's Hours": "mens", 
             "Money Talk": "moneytalk", "National Geographic": "nationalgeo", "Newsweek": "newsweek", "New Yorker": "newyorker", 
             "New York Times": "nyt", "Tennessean Opinions": "opinion", "People": "people", "Pet Potpourri": "pet", "PNS 2025 Talks": "pnstalks", 
             "PNS Daily Newscast": "pns", "PNS Yonder Report": "pnsyonder", "Poetry in the Air": "poetry", "Prevention": "prevention", 
             "Reader's Digest": "readersdigest", "Rolling Stone": "rollingstone", "Nashville Scene": "scene", "New Scientist": "science", 
             "Smithsonian": "smithsonian", "Spotlight on Sports": "sports", "Tennessean": "tennessean", "Time": "time", "Town & Country": "town", 
             "Vanity Fair": "vanity", "Wired": "wired", "Woman's World": "woman", "Wall Street Journal": "wsj"}
    return {"shows": shows}

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
    current_time = time.time()
    cache_time = 120 # how long (in seconds) do we want to keep cached data before fetching again
    # if we have cached data and it has been less than 60 seconds since we cached it
    if weather_cache["data"] and (current_time - weather_cache["timestamp"] < cache_time):
        return weather_cache["data"]
    
    url = "https://api.weather.gov/stations/KBNA/observations/latest"
    # NWS asks that you identify yourself. Include the other headers so they send us fresh/correct data
    header = {"User-Agent": "NashvilleTalkingLibraryMobileApp (nashvilletalkinglibrary@gmail.com)",
            "Accept": "application/geo+json",
            "Accept-Language": "en-US,en;q=0.8"
            }
    request = requests.get(url=url, headers=header)
    try:
        weather = request.json()
        temp_c = weather["properties"]["temperature"]["value"]
        temp_f = int(temp_c * 9/5 + 32) # comes from NWS in celsius

        response = {'temp': temp_f}

        # update cache
        weather_cache["data"] = response
        weather_cache["timestamp"] = current_time
    except:
        response = 'failed', 500
    return response