import json

#json.loads(string) = dict (json)
#json.dumps(dic) = string

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
json_dict = {"first_name": "Guido", "last_name":"Rossum"}
bad_json_string = "{"first_name": "Guido", "last_name":"Rossum"}""


print(json_dict["first_name"])


parsed_json = json.loads(json_string)

print(type(parsed_json))
print(parsed_json['first_name'])

d = {
    'first_name': 'Guido',
    'second_name': 'Rossum',
    'titles': ['BDFL', 'Developer'],
}

print(json.dumps(d))
print(d)

#print(json.dumps(d)["first_name"])

print(type(d))
print(type(json.dumps(d)))

print(d['titles'])

print(d.get("titles"))
