from os import confstr
import socketio
import socket
import utils
import time
import json
import actionFactory
import serverComms
import logging

# standard Python
sio = socketio.Client()
hostname = socket.gethostname()
CONFIG = json.load(open('client_config.json','r'), object_hook=utils.customJsonDecoder)
server_ip= CONFIG.server_ip
server_port= CONFIG.server_port
server= 'http://{0}:{1}'.format(server_ip,str(server_port))

logging.basicConfig(filename='ramNET_Client.log', 
level=logging.INFO, 
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

@sio.event
def connect():
    print(utils.print_status(hostname , server , "connected"))
    sio.emit('login', {'userKey': 'streaming_api_key'})

@sio.event
def connect_error(data):
    print(utils.print_status(hostname , server , "Connection Failed"))
    print("The connection failed!. Retrying in 10 seconds.. ")
    time.sleep(10)
    try:
        sio.connect(server)
    except:
        pass


@sio.on(hostname)
def on_message(data):
    js = json.loads(data)
    action = js['action']
    actionObj = actionFactory.getActionObject(action, js)
    actionObj.process()
    comm = serverComms.ServerCommunication(server_ip,server_port)
    status = comm.send_frame(actionObj.id , actionObj.frame)
    print("Served requestId "+ actionObj.id )
    return status



sio.connect(server)
