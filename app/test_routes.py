import os

import pytest
import requests

from app import app
from app.sql import SQL
from app.ev import EV
from flask.testing import FlaskClient


@pytest.fixture
def client():
    app.testing = True
    client =  app.test_client()
    yield client
    
    try:
        os.remove("banner.db")
    except:
        pass
    
'''
GET real GET routes
'''

def test_home_get_1(client: FlaskClient):
    '''home/landing route'''
    resp = client.get('/')
    assert resp.status_code == 200

def test_booth_get_1(client: FlaskClient):
    response = client.get('/booth')
    assert response.status_code == 200

def test_boothBanner_get_1(client: FlaskClient):
    response = client.get('/booth/banner')
    assert response.status_code == 200

def test_boothSchedule_get_1(client: FlaskClient):
    response = client.get('/booth/schedule')
    assert response.status_code == 200

def test_status_get_1(client: FlaskClient):
    '''reuiqres auth'''
    response = client.get('/status')
    assert response.status_code == 401

'''
GET non-GET routes
'''

def test_boothData_1(client: FlaskClient):
    '''post only'''
    response = client.get('/booth/data')
    assert response.status_code == 405

def test_statusPing_1(client: FlaskClient):
    '''post only'''
    response = client.get('/status/ping')
    assert response.status_code == 405

def test_statusUserAgent_1(client: FlaskClient):
    '''post only'''
    response = client.get('/status/useragent')
    assert response.status_code == 405

def test_statusStream_1(client: FlaskClient):
    '''post only'''
    response = client.get('/status/stream')
    assert response.status_code == 405

def test_fake_url_1(client: FlaskClient):
    '''non routes should return 404 no matter the request type'''
    response = client.get('/maaah')
    assert response.status_code == 404

def test_fake_url_2(client: FlaskClient):
    '''we always want to include '404' somewhere on the page, for clarity to user'''
    response = client.get('/maaah')
    assert '404' in response.text

def test_stream_get_1(client: FlaskClient):
    response = client.get('/stream')
    assert response.status_code == 405

def test_twilio_get_1(client: FlaskClient):
    response = client.get('/twilio')
    assert response.status_code == 405

'''
POST real POST routes
'''

def test_banner_post(client: FlaskClient):
    '''this is NOT testing whether the credentials are correct! only if the post request is formatted correctly'''
    response = client.post('/booth/banner', data=
                           {"password": "something",
                            "bannerMessage": "something",
                            "bannerColor": "something",
                            })
    assert response.status_code == 200

def test_banner_post_no_data(client: FlaskClient):
    '''should fail if form data is missing'''
    response = client.post('/booth/banner')
    assert response.status_code == 400

def test_banner_post_missing_data(client: FlaskClient):
    '''should fail if SOME form data is missing'''
    response = client.post('/booth/banner', data={"user": ""})
    assert response.status_code == 400

def test_banner_message(client: FlaskClient):
    message = "some message here"
    response = client.post('/booth/banner', data=
                           {"password": EV().BF_pass,
                            "bannerMessage": message,
                            "bannerColor": "something"
                            })
    assert SQL().read_message() == message

def test_weather_post_1(client: FlaskClient):
    '''if for some reason the NWS is having issues, we don't want the tests to fail'''
    response = client.post('/booth/weather')
    weather_endpoint = requests.get("https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly")
    if weather_endpoint.status_code != 200:
        assert True
        return
    assert response.status_code == 200

def test_weather_post_2(client: FlaskClient):
    '''if for some reason the NWS is having issues, we don't want the tests to fail'''
    response = client.post('/booth/weather')
    weather_endpoint = requests.get("https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly")
    if weather_endpoint.status_code != 200:
        assert True
        return
    assert response.content_type == 'application/json'

def test_booth_banner_content_post_1(client: FlaskClient):
    response = client.post('/booth/banner/content')
    assert response.status_code == 200

def test_booth_banner_content_post_2(client: FlaskClient):
    response = client.post('/booth/banner/content')
    assert response.content_type == 'application/json'

def test_stream_post_1(client: FlaskClient):
    response = client.post('/stream')
    assert response.status_code == 200

def test_stream_post_2(client: FlaskClient):
    '''should return plain text'''
    response = client.post('/stream')
    assert 'text/html' in response.content_type

def test_stream_status_post_1(client: FlaskClient):
    response = client.post('stream/status')
    assert response.status_code == 200

def test_stream_status_post_2(client: FlaskClient):
    response = client.post('stream/status')
    assert response.content_type == 'application/json'

def test_twilio_post_1(client: FlaskClient):
    response = client.post('/twilio')
    assert response.status_code == 200

def test_twilio_post_2(client: FlaskClient):
    response = client.post('/twilio')
    assert 'text/html' in response.content_type

def test_holiday_post_1(client: FlaskClient):
    response = client.post('/booth/holiday')
    assert response.status_code == 200

def test_holiday_post_2(client: FlaskClient):
    response = client.post('/booth/holiday')
    assert response.content_type == 'application/json'

def test_statusStream_post_1(client: FlaskClient):
    '''requires auth'''
    response = client.post('status/stream')
    assert response.status_code == 401

def test_statusStream_post_2(client: FlaskClient):
    '''requires auth. if auth not present, returns plain text response'''
    response = client.post('status/stream')
    assert 'text/html' in response.content_type

def test_statusPing_post_1(client: FlaskClient):
    '''requires auth'''
    response = client.post('status/ping')
    assert response.status_code == 401

def test_statusMounts_post_1(client: FlaskClient):
    '''requires auth'''
    response = client.post('status/mounts')
    assert response.status_code == 401

def test_statusUserAgent_post_1(client: FlaskClient):
    '''requires auth'''
    response = client.post('status/useragent')
    assert response.status_code == 401

'''
POST non-POST routes
'''

def test_home_post_1(client: FlaskClient):
    '''should fail for non-POST routes'''
    response = client.post('/')
    assert response.status_code == 405

def test_booth_post_1(client: FlaskClient):
    '''should fail for non-POST routes'''
    response = client.post('/booth')
    assert response.status_code == 405

def test_status_post_1(client: FlaskClient):
    '''should fail for non-POST routes'''
    response = client.post('/status')
    assert response.status_code == 405