from collections import namedtuple

def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())