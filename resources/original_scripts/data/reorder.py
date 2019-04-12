import json

names = open("missing_names.json", 'r')
name_list = json.load(names)

fake_skim = []

for name in name_list['names']:
    fake_skim.append({"id":name})

f = open("missing_names_skim.json", 'a')
f.write(json.dumps(fake_skim))
f.close()
