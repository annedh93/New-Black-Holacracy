import json
import requests

api_token = '3dcf31b52820a0ad8e2841039768cb59f8e20874'
api_url_circles = "https://api.glassfrog.com/api/v3/circles"
api_url_people = "https://api.glassfrog.com/api/v3/people"

headers = {'Content-Type': 'application/json',
           'X-Auth-Token': api_token}

# Load in json script with circle
response_circles = requests.get(api_url_circles, headers = headers)
circles = json.loads(response_circles.text)

# Load in json script with people
response_people = requests.get(api_url_people, headers = headers)
people = json.loads(response_people.text)

circles_dict = {}
roles_dict = {}

for i in range(len(circles['linked']['roles'])):
    supporting_circle_id = circles['linked']['roles'][i]['links']['supporting_circle']
    role_id = circles['linked']['roles'][i]['id']
    role_name = circles['linked']['roles'][i]['name']

    # print(supporting_circle_id, role_name)

    if supporting_circle_id not in circles_dict and supporting_circle_id is not None:
        circles_dict[supporting_circle_id] = role_name 
    
    if role_id not in roles_dict and role_id is not None:
        roles_dict[role_id] = role_name
    

people_dict = {}

for i in range(len(people['people'])):
    people_id = people['people'][i]['id']
    people_name = people['people'][i]['name']

    if people_id not in people_dict and people_id is not None:
        people_dict[people_id] = people_name

holacracy = circles_dict.copy()

for i in circles_dict:
    holacracy[i] = {'name': circles_dict[i]}
    holacracy[i]['roles'] = {}

for i in range(len(circles['linked']['roles'])):
    circle_id = circles['linked']['roles'][i]['links']['circle']
    role_id = circles['linked']['roles'][i]['id']
    role_name = circles['linked']['roles'][i]['name']
    people_id = circles['linked']['roles'][i]['links']['people']

    if circle_id is not None:
        holacracy[circle_id]['roles'][role_id] = {'name': role_name}
        holacracy[circle_id]['roles'][role_id]['people'] = {}
        for j in range(len(people_id)):
            holacracy[circle_id]['roles'][role_id]['people'][people_id[j]] = people_dict[people_id[j]]

# Builds dictionary with the following nested structure: circle id, role id and people id
holacracy2 = {}

for i in circles_dict:
    holacracy2[i] = {}

for i in range(len(circles['linked']['roles'])):
    circle_id = circles['linked']['roles'][i]['links']['circle']
    role_id = circles['linked']['roles'][i]['id']
    role_name = circles['linked']['roles'][i]['name']
    people_id = circles['linked']['roles'][i]['links']['people']

    if circle_id is not None:
        holacracy2[circle_id][role_id] = people_id 

# [people_dict[x] for x in mykeys]
