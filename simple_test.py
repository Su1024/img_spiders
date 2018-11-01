import requests

response = requests.get(url='http://www.sj33.cn/')
print(response.content)
