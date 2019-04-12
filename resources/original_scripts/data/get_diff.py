import json

repos = open("2019-04-01_npm_repos_curated.txt", 'r')
skim = open("2019-04-01_npm_skim.json", 'r')

missing_repo_names = []

skim_json = json.load(skim)

package_names = set()

counter = 0

for package in skim_json:
    counter += 1
    if counter % 1000 == 0:
        print(counter)
    package_names.add(package["id"])

counter = 0

print("done creating list")

for line in repos:
    counter += 1
    if counter % 1000 == 0:
        print(counter)
    line_json = json.loads(line)
    name = line_json["name"]

    if name in package_names:
        package_names.remove(name)

final_names = {"names" : list(package_names)}

f = open("missing_names.json", 'a')
f.write(json.dumps(final_names))
f.close()
