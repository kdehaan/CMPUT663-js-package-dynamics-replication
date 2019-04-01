import requests
import json

def get_package_names(stable, offset):
    """
    stable: boolean isstable???? lmao
    offset: the current offset to be using
    """
    stability='stable' if stable else 'unstable'
    urlstr = 'https://registry.npmjs.org/-/v1/search?text=is:{stability}&size=250&from={offset}'.format(stability=stability, offset=offset)
    r = requests.get(urlstr)
    if r.status_code != 200:
        raise Exception('Failed to get on query: {stability} with offset {offset}'.format(stability=stability, offset=offset))

    data = r.json()

    names = []

    for object in data['objects']:
        names.append(object['package']['name'])

    f = open('{stability}-{offset}.json'.format(stability=stability, offset=offset), 'w')

    f.write(json.dumps(names))

    f.close()

get_package_names(True, 0)
