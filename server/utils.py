from collections import namedtuple
from datetime import datetime
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

def getIndexOfObject(Arr:list , key , value):
    
    for items in Arr:
        if(items[key]==value):
            return Arr.index(items)
    return -1

def addToActiveClient(Arr:list , vmName, id , processName ):
    index = getIndexOfObject(Arr, 'hostName', vmName)
    if(index != -1):
        if(Arr[index].get('monitoring') == None):
            Arr[index]['monitoring']=[]
        Arr[index]['monitoring'].append({
            'id': id, 
            'processName':processName,
            'startedAt': str(datetime.now())
        })
    return Arr

def removeFromActiveClient(Arr:list , vmName,  id ):
    try:
        index = getIndexOfObject(Arr, 'hostName', vmName)
        if(index != -1):
            for items in Arr[index]['monitoring']:
                if(items['id'] == id ):
                    idx = Arr[index]['monitoring'].index(items)
                    del Arr[index]['monitoring'][idx]
        return True
    except:
        print("Failure in updating ACTIVE CLIENTS")
        return False    

