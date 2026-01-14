import requests

url = "http://192.222.54.121:8060/generate"
data = {
    "prompt": "Generate a free response question on recursion"
}

response = requests.post(url, json=data)
print(response.json())
