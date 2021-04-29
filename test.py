import requests

BASE = "http://127.0.0.1:5000/"
url='google.com'
response = requests.get(BASE+"/bolster/"+url)

#response = requests.get(BASE+"/video/123")

print(response.json())