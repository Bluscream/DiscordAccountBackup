import json, os
from datetime import datetime

def log(*message):
    print(datetime.now(), *message)

def saveJSON(file, data, encoder = None):
    dir = os.path.dirname(file)
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
    with open(file, 'w') as outfile:
        json.dump(data, outfile, cls=encoder, indent=4)
def loadJSON(file, default):
    if not os.path.isfile(file):
        return default
    with open(file) as json_file:
        return json.load(json_file)

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__