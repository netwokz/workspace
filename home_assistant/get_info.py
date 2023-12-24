import os
from homeassistant_api import Client

URL = '<API BASE URL>'
TOKEN = '<LONG LIVED ACCESS TOKEN>'

# Assigns the Client object to a variable and checks if it's running.
client = Client(URL, TOKEN)