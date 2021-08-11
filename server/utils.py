from collections import namedtuple
import json
import pandas

def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())

def getStats(filePath):

    js = json.load(open(filePath))
    df = pandas.DataFrame(js['memory_usage'])
    df.quantile(0.1)
    out={
        "mean":df.mean()[1],
        "median":df.median()[1],
        "max":df.max()[1],
        "min":df.min()[1],
        "percentile":{
            "0.1":df.quantile(0.1)[1],
            "0.2":df.quantile(0.2)[1],
            "0.3":df.quantile(0.3)[1],
            "0.7":df.quantile(0.7)[1],
            "0.8":df.quantile(0.8)[1],
            "0.9":df.quantile(0.9)[1]
        }
    }
    return out
