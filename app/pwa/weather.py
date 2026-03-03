import time

from diskcache import Cache
import requests

weather_cache = Cache("weather_cache")

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
    temp = weather_cache.get(station)
    print(f"retrieving cache: {station}: {temp}")
    if temp:
        return temp
        
    return False

def append_or_update_cache(station: str, temp: int):
    print(f"adding {station}: {temp}")
    '''If we have already cached the station, update the temp. If we have not yet cached this station, create a new item for it.'''
    weather_cache.add(key=station, value=temp,  expire=120)