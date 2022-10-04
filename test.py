import requests

url = "http://localhost:8001/chitchat"
contexts = ["こんにちは。少しお話、できますか？", "いいですよ", "実は悩みが"]

data = {"contexts": contexts}
response = requests.post(url, json=data)
print(response.text)
