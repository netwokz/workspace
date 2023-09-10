import datetime as dt
import requests
import json

COUNTRY = 'us'
STATE = 'AZ'
CITY = 'Buckeye'
ZIP = '85326'

DEGREE = u'\N{DEGREE SIGN}'
FILE_PATH = 'C:\\Users\\deanejst\\Documents\\code\\python\\'
API_KEY = open(FILE_PATH + 'weather_api_key', 'r').read()
FILENAME = "last_response.json"
BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={ZIP},{COUNTRY}&appid={API_KEY}"

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
    with open(FILE_PATH + FILENAME, 'w') as json_file:
        json.dump(response,json_file)
    return response

def old_response():
    global response
    with open(FILE_PATH + FILENAME, 'r') as json_file:
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


temp_kelvin = report['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = report['main']['feels_like']
feels_like_celsius, feels_like_fahrenheit  =kelvin_to_celsius_fahrenheit(feels_like_kelvin)
humidity = report['main']['humidity']
description = report['weather'][0]['description']
sunrise_time = dt.datetime.utcfromtimestamp(report['sys']['sunrise'] + report['timezone'])
sunset_time = dt.datetime.utcfromtimestamp(report['sys']['sunset'] + report['timezone'])


print(f"Temperature in {CITY}: {temp_fahrenheit:.0f}{DEGREE}F or {temp_celsius:.0f}{DEGREE}C")
print(f"Temperature in {CITY} feels like: {feels_like_fahrenheit:.0f}{DEGREE}F or {feels_like_celsius:.0f}{DEGREE}C")
print(f"Humidity in {CITY}: {humidity}%")
print(f"Weather in {CITY}: {description}")
print(f"Sunrise in {CITY} at {sunrise_time} local time.")
print(f"Sunset in {CITY} at {sunset_time} local time.")

