import requests

url = "https://superhero-search.p.rapidapi.com/api/"

hero = input("Enter the superhero's / villain's name: ")
params = {"hero": hero}

headers = {
    'x-rapidapi-host': "superhero-search.p.rapidapi.com",
    'x-rapidapi-key': "key_here"
}

response = requests.get(url, headers=headers, params=params)
json_data = response.json()

if json_data['biography']['alignment'] == 'good':
    print(f"Hero's name: {json_data['name']}")
else:
    print(f"Villain's name: {json_data['name']}")
print(f"Real name: {json_data['biography']['fullName']}")
print(f"Image: {json_data['images']['lg']}")
