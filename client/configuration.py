import json
from collections import namedtuple  

def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())

CONFIG = json.load(open('client_config.json','r'), object_hook=customJsonDecoder)