import amzn_requests

URL = "https://phonetool.amazon.com/users/search?query={name}"
url = URL.format(name="deanejst")
response = amzn_requests.amzn_requests(url)
print(response.status_code)  # 200
print(response.json())
