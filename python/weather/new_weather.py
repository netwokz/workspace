import datetime as dt
import requests
import json

COUNTRY = 'us'
STATE = 'AZ'
CITY = 'Buckeye'
ZIP = '85326'

DEGREE = u'\N{DEGREE SIGN}'
#API_KEY = open('api_key', 'r').read()
FILENAME = "new_response.json"
BASE_URL = "https://api.tomorrow.io/v4/timelines?location=6287603f8f191300088f84d9&fields=temperature&fields=temperatureApparent&fields=humidity&fields=windSpeed&fields=windDirection&fields=windGust&fields=weatherCode&units=imperial&timesteps=current&timezone=America%2FPhoenix&apikey=VMBO9JZIll1pdp0B77KEI8BR9kFJOysN"

headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip"
    }

FIRST_RUN = True
global TIME_STAMP

def check_first_run():
    global TIME_STAMP
    global FIRST_RUN
    if(FIRST_RUN):
        new_response()
        TIME_STAMP = dt.datetime.now()
        FIRST_RUN = False

def new_response():
    global response
    response = requests.get(BASE_URL).json()
    with open(FILENAME, 'w') as json_file:
        json.dump(response,json_file)
    return response

def old_response():
    global response
    with open(FILENAME, 'r') as json_file:
        response = json.load(json_file)
    return response

def check_response():
    global TIME_STAMP
    global report
    now = dt.datetime.now()
    delta = now - TIME_STAMP
    if((delta.total_seconds() / 60) > 10):
        TIME_STAMP = now
        report = new_response()
    else:
        report = old_response()

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

check_first_run()
#print(TIME_STAMP)
check_response()

temp = report['data']['timelines'][0]['intervals'][0]['values']['temperature']
temperature_apparent = report['data']['timelines'][0]['intervals'][0]['values']['temperatureApparent']
humidity = report['data']['timelines'][0]['intervals'][0]['values']['humidity']
weather_code = report['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
wind_direction = report['data']['timelines'][0]['intervals'][0]['values']['windDirection']
wind_gust = report['data']['timelines'][0]['intervals'][0]['values']['windGust']
wind_speed = report['data']['timelines'][0]['intervals'][0]['values']['windSpeed']
print(temp)
print(temperature_apparent)
print(humidity)
print(weather_code)
print(wind_direction)
print(wind_gust)
print(wind_speed)

