# import requests module
import requests

# Making a get request


def get_random_quote():
    response = requests.get("https://api.unsplash.com/photos/?client_id=TtmRXOFV1wsIFLpy-OxN9YZuUbkj7wnJBqVRbFgR-4k").json()
    quote = response[0]["q"] + " - " + response[0]["a"]
    # print(f"{quote}")
    return quote


print(get_random_quote())
