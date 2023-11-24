import requests

id = "test"
data = {"rgb": "255,128,128"}
r = requests.post("http://localhost:8000/api/post/{}".format(id), json=data)

id = "test"
r = requests.get("http://localhost:8000/api/get/{}".format(id))
print(r.text)
