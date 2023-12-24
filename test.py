import os

from homeassistant_api import Client
from requests import get, post

# url = "http://10.10.10.7:8123/api/services/fan/turn_on"
# state_url = "http://10.10.10.7:8123/api/states"
# headers = {
#     "Authorization": "Bearer meyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3YzdhMTEwZTU4ZGY0NDBkYjJmNzU2MjVmMmEzN2I1MSIsImlhdCI6MTcwMzM1Mzk5OSwiZXhwIjoyMDE4NzEzOTk5fQ.ricBuxIHxxiArVrvZ14cxvtRfLIecKsungSATXumAfw",
#     "Content-Type": "application/json",
# }

# bedroom_light_id = "177fba49faacb5654f86e0c0c2da0a46"
# data = {"entity_id": "fan.fan2"}

# response = get(state_url, headers=headers)
# print(response.text)


URL = "http://10.10.10.7:8123/api"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0ZmJhOWJiNDBmYTQ0OTM3OWIyYTZmYmY3NWFiYTQxNSIsImlhdCI6MTcwMzM1ODc1MCwiZXhwIjoyMDE4NzE4NzUwfQ.QUC8OEM9O7uW23LOanCWDXmR-hGfn-ajwJKthoBtRpc"

# Assigns the Client object to a variable and checks if it's running.
client = Client(URL, TOKEN)

# service = client.get_domain("light")  # Gets the light service domain from Home Assistant

# service.turn_on(entity_id="light.my_living_room_light")
# Triggers the light.turn_on service on the entity `light.my_living_room_light`

# You can also initialize Client before you use it.
entity_groups = client.get_entities()
for entity in entity_groups:
    # print(entity)
    pass
# {'person': <Group person>, 'zone': <Group zone>, ...}

states = client.get_states()
# [<State "above_horizon" entity_id="sun.sun">, <State "zoning" entity_id="zone.home">,...]
for entity_state in states:
    # if entity_state.entity_id == "light.":
    print(entity_state.entity_id, "\n")


# client = Client("https://foobarhomeassistant.duckdns.org:8123/api", "mylongtokenpasswordthingyfoobar")
# # In order to activate the requests session you to use the Client context manager like so.
# # Using it as a context manager will automatically close the session when you're done with it.
# # But also will *ping* your Home Assistant instance to make sure it's running.
# with client:
#     while True:
#         sun = client.get_entity(entity_id="sun.sun")
#         state = sun.get_state()  # Because requests are cached we reduce bandwidth usage :D
#         # Cache expires every 30 seconds by default.
#         if state.state == "below_horizon":
#             difference = datetime.now() - state.last_updated
#             print("Sun set", difference.seconds, "seconds ago.")
#             break
