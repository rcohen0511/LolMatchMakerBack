import json
from pprint import pprint

with open('championFull.json') as data_file:
    data = json.load(data_file)

pprint(data["data"]["Aatrox"]['spells']['AatroxQ'])
print(data["data"])