import os


from homeassistant_api import Client, State
from requests import get, post

URL = "http://10.10.10.7:8123/api"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0ZmJhOWJiNDBmYTQ0OTM3OWIyYTZmYmY3NWFiYTQxNSIsImlhdCI6MTcwMzM1ODc1MCwiZXhwIjoyMDE4NzE4NzUwfQ.QUC8OEM9O7uW23LOanCWDXmR-hGfn-ajwJKthoBtRpc"

client = Client(URL, TOKEN)

# service = client.get_domain("light")  # Gets the light service domain from Home Assistant

# service.turn_on(entity_id="light.my_living_room_light")
# Triggers the light.turn_on service on the entity `light.my_living_room_light`

# You can also initialize Client before you use it.
entity_groups = client.get_entities()
for entity in entity_groups["sensor"]:
    # print(entity)
    pass

states = client.get_states()
for entity_state in states:
    if entity_state.entity_id.startswith("light.wled"):
        # print(entity_state.entity_id)
        pass


desk_wled = client.get_entity(entity_id="light.wled")
# print(desk_wled)
