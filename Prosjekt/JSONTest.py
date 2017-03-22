import json
'''

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
'''
json_dict2 = {"response": "success"}
json_dict21 = {"response": "error"}
json_dict3 = {"response": "history", "last_name":"Rossum"}
jsonarray = []
jsonarray.append(json.dumps(json_dict2))
jsonarray.append(json_dict21)
jsonarray.append(json_dict3)
print(type(jsonarray), jsonarray)
print(type(jsonarray[0]), jsonarray[0])
print(type(json.loads(jsonarray[0])), json.loads(jsonarray[0]))
print(json.loads(jsonarray[0])["response"])

jsondictarray = {"content": jsonarray}
jsondictarray = json.dumps(jsondictarray)
print(type(jsondictarray), jsondictarray)
print(type(jsondictarray[0]), jsondictarray[0])
print(type(json.loads(jsondictarray[0])), json.loads(jsondictarray[0]))
print(json.loads(jsondictarray[0])["content"])


TypeError: the JSON object must be str, not 'list'
