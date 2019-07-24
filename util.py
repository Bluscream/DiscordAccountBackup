import json, os
from datetime import datetime
from urllib import request

def log(*message):
    print(datetime.now(), *message)

def createDirFor(path, isDir : bool = False):
    if not isDir: path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def saveJSON(file, data, encoder = None):
    createDirFor(file)
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

def downloadFile(url, output_file):
    createDirFor(output_file)
    request.urlretrieve(url, output_file)