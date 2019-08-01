import json
import requests

api_token = '3dcf31b52820a0ad8e2841039768cb59f8e20874'
api_url_circles = "https://api.glassfrog.com/api/v3/circles"
api_url_roles = "https://api.glassfrog.com/api/v3/roles"
api_url_people = "https://api.glassfrog.com/api/v3/people"

headers = {'Content-Type': 'application/json',
           'X-Auth-Token': api_token}

# Load in json script with circle
response_circles = requests.get(api_url_circles, headers = headers)
circles = json.loads(response_circles.text)

# Load in json script with roles
response_roles = requests.get(api_url_roles, headers = headers)
roles = json.loads(response_roles.text)

# Load in json script with people
response_people = requests.get(api_url_people, headers = headers)
people = json.loads(response_people.text)

circles_dict = {}
roles_dict = {}
purpose_dict = {}
account_dict = {}

for i in range(len(circles['linked']['roles'])):
    supporting_circle_id = circles['linked']['roles'][i]['links']['supporting_circle']
    role_id = circles['linked']['roles'][i]['id']
    role_name = circles['linked']['roles'][i]['name']
    purpose = circles['linked']['roles'][i]['purpose']
    accountability = circles['linked']['roles'][i]['links']['accountabilities']

    if supporting_circle_id not in circles_dict and supporting_circle_id is not None:
        circles_dict[supporting_circle_id] = role_name 
    
    if role_id not in roles_dict and role_id is not None:
        roles_dict[role_id] = role_name
        purpose_dict[role_id] = purpose
        account_dict[role_id] = accountability
    
accountabilities_dict = {}

for i in range(len(roles['linked']['accountabilities'])):
    accountability_id = roles['linked']['accountabilities'][i]['id']
    accountability_name = roles['linked']['accountabilities'][i]['description']

    if accountability_id not in accountabilities_dict and accountability_id is not None:
        accountabilities_dict[accountability_id] = accountability_name

people_dict = {}

for i in range(len(people['people'])):
    people_id = people['people'][i]['id']
    people_name = people['people'][i]['name']

    if people_id not in people_dict and people_id is not None:
        people_dict[people_id] = people_name

# Builds dictionary with the following nested structure: circle id, role id and people id
holacracy = {}

for i in circles_dict:
    holacracy[i] = {}

for i in range(len(circles['linked']['roles'])):
    circle_id = circles['linked']['roles'][i]['links']['circle']
    role_id = circles['linked']['roles'][i]['id']
    people_id = circles['linked']['roles'][i]['links']['people']

    if circle_id is not None:
        holacracy[circle_id][role_id] = people_id 

for m in range(len(holacracy)):
    circle_id = list(circles_dict.keys())[m]
    for k in range(len(holacracy[circle_id])):
        role_id = list(holacracy[circle_id].keys())[k]
        people_id = holacracy[circle_id][role_id]

        role = roles_dict[role_id]
        role_ = role
        role_ = role_.replace(".", "")
        role_ = role_.replace(" ", "_")
        role_ = role_.replace("/", "_")

        accountability_id = account_dict[role_id]
        accountabilities = [accountabilities_dict[x] for x in accountability_id]
    
        purpose = purpose_dict[role_id]

        people = [people_dict[x] for x in people_id]

        with open('C:/Users/anned/Documents/New Black/Holocracy/Glassfrog Git/Roles/' + 
          circles_dict[circle_id] + '/' + role_ + '.md', 'w') as f:
            data = """#Role: %s \n\n#Purpose: %s \n\n#Accountabilities: %s \n\n#People: %s"""
            f.write(data % (role, purpose, accountabilities, people))