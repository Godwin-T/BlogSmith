import json
import requests

url = "http://127.0.0.1:9696/respond"
query = input("Enter the blogpost content topic or idea\n")
user_input = {"query": query}
output = requests.post(url, json=user_input).json()

print(output["response"])
