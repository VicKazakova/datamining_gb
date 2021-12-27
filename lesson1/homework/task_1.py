import json

import requests

# user = 'VicKazakova'
user = input('Enter the username: ')
url = 'https://api.github.com/users/' + user + '/repos'
response = requests.get(url)
json_data = response.json()

for i in range(0, len(json_data)):
    print("Project Number:", i + 1)
    print("Project Name:", json_data[i]['name'])
    print("Project URL:", json_data[i]['svn_url'], "\n")

with open('repos.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f)
