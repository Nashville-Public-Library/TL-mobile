import time

import requests

weather_cache:list = []

def get_weather(station):
    cached_temp = check_cache(station=station)
    if cached_temp:
        return {"temp": cached_temp}
    
    url = f"https://api.weather.gov/stations/{station}/observations/latest"
    # NWS asks that you identify yourself. Include the other headers so they send us fresh/correct data
    header = {"User-Agent": "NashvilleTalkingLibraryMobileApp (nashvilletalkinglibrary@gmail.com)",
            "Accept": "application/geo+json",
            "Accept-Language": "en-US,en;q=0.8"
            }
    try:
        request = requests.get(url=url, headers=header)
        weather = request.json()
        temp_c = weather["properties"]["temperature"]["value"]
        temp_f = int(temp_c * 9/5 + 32) # comes from NWS in celsius

        append_or_update_cache(station=station, temp=temp_f)

        return {"temp": temp_f}, 200
    
    except:
        return {"temp": None}, 500

def check_cache(station):
    print("checking cache for " + station)
    for id in weather_cache:
        print(id["station"] + " time: " + str(time.time() - id["time"]))
        if (id["station"] == station) and ((time.time() - id["time"]) < 120):
            temp = id["temp"]   
            print(f"returning cached result for {station}: " + str(temp))
            print(weather_cache)
            return temp
    return False

def append_or_update_cache(station: str, temp: int):
    '''If we have already cached the station, update the temp. If we have not yet cached this station, create a new item for it.'''
    now = time.time()
    for id in weather_cache:
        if id["station"] == station:
            id["temp"] = temp
            id["time"] = now
            print("cache updated")
            print(weather_cache)
            return
    weather_cache.append({"station": station, "temp": temp, "time": now})
    print("cache appended")
    print(weather_cache)