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
        self.parameters = incoming_frame['params']
    
    

class Action_GET_PROCESS_LIST(UnitMessage):
    def process(self):
        try:
            x=utils.getProcess_list()
            self.frame['status']='OK'
            self.frame['payload']=x
        except:
            self.frame['status']='FAIL'
            self.frame['payload']=None









class Action_Exception(UnitMessage):
    def process(self):
        self.frame['status']='FAIL'
        self.frame['payload'] = "Error , Unsupported Operation"

def getActionObject(action, message ):
    if(action == 'GET_PROCESS_LIST'):
        return Action_GET_PROCESS_LIST(message)
    else:
        return Action_Exception(message)