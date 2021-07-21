import utils


message_frame={
    "id":None,
    "action":None,
    "status":None,
    "payload":None
}

class UnitMessage():
    def __init__(self, incoming_frame):
        self.id = incoming_frame['id']
        self.frame = message_frame
        self.frame['id'] = self.id
        self.frame['action']= incoming_frame['action']
        self.frame['parameters'] = incoming_frame['params']
    
    

class Action_GET_PROCESS_LIST(UnitMessage):
    def process(self):
        try:
            x=utils.getProcess_list()
            self.frame['status']='OK'
            self.frame['payload']=x
        except:
            self.frame['status']='FAIL'
            self.frame['payload']=None


class Action_START_MONITORING(UnitMessage):
    def process(self):
        try:
            process_name = self.frame['parameters']["process_name"]
            latest = self.frame['parameters']["latest"]
            pId=utils.get_pid(process_name , latest = latest)
            if(pId==-1):
                raise Exception("Unable to find process: "+process_name)
            monitoring_pId = utils.start_monitoring(pId , self.id , self.frame["parameters"]["polling_interval"])
            self.frame['status']='OK'
            self.frame['payload']={
                "monitoring_pId":monitoring_pId
            }
        except Exception as e:
            self.frame['status']='FAIL'
            self.frame['payload']=str(e)




class Action_Exception(UnitMessage):
    def process(self):
        self.frame['status']='FAIL'
        self.frame['payload'] = "Error , Unsupported Operation"

def getActionObject(action, message ):
    if(action == 'GET_PROCESS_LIST'):
        return Action_GET_PROCESS_LIST(message)
    elif(action == 'START_MONITORING'):
        return Action_START_MONITORING(message)
    else:
        return Action_Exception(message)