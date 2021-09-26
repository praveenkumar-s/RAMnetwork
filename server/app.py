import json
from os import path
import re
from requests.sessions import Request
import utils
from types import MethodDescriptorType
import uuid
from flask import Flask, render_template, jsonify
from flask.globals import request
from flask_socketio import SocketIO, emit
from uuid import uuid4
import sys
import requests
import cachehelper
import socketIO_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
message_frame = {
    "id": None,
    "action": None,
    "params": {}
}
CONFIG = json.load(open('server_config.json', 'r'),
                   object_hook=utils.customJsonDecoder)
CACHE = cachehelper.CacheProvider(
    CONFIG.redis_cache.server, CONFIG.redis_cache.port)

ACTIVE_CLIENTS = []

@app.route('/')
def index():
    return "hello world"


@app.route("/sendJson/<topic>", methods=['POST'])
def sendjson(topic):
    json_data = request.get_json()
    msg = json.dumps(json_data)
    socketio.emit(topic, msg)
    return "OK"


@app.route('/api/<vm_name>/listProcess', methods=['GET'])
def getProcessList(vm_name):
    vm_name = vm_name.lower()
    id = str(uuid4())
    msg = dict(message_frame)
    msg["action"] = "GET_PROCESS_LIST"
    msg['id'] = id
    socketio.emit(vm_name, json.dumps(msg))
    process_list = CACHE.getCachedJsonWithRetry(id, 10)
    if(process_list is None):
        return "client not found or not running",404
    return jsonify(process_list)


@app.route('/api/save/<id>', methods=['POST'])
def saveResponse(id):
    json_data = request.get_json()
    CACHE.setCacheJson(id, json_data)
    return 'OK', 200

@app.route('/api/<vm_name>/startMonitoring',methods=['POST'])
def startMonitoring(vm_name):
    vm_name = vm_name.lower()
    id = str(uuid4())
    json_d = request.get_json()
    try:
        assert(json_d.get('process_name') != None)
        assert(json_d.get('polling_interval') != None)
        assert(json_d.get('latest') != None)
    except:
        return "error: "+sys.exc_info() , 400
    msg = dict(message_frame)
    msg["action"] = "START_MONITORING"
    msg['id'] = id
    msg['params']=json_d
    socketio.emit(vm_name, json.dumps(msg))
    response = CACHE.getCachedJsonWithRetry(id , 10)
    if(response['status'] != 'FAIL'):
        utils.addToActiveClient(ACTIVE_CLIENTS , vm_name , id , json_d.get('process_name'))
    return jsonify({
        "id":id,
        "status": response['status'],
        "payload": response['payload']  
    })

@app.route('/api/<vm_name>/stopMonitoring', methods=['POST'])
def stopMonitoring(vm_name):
    vm_name = vm_name.lower()
    json_data = request.get_json()
    try:
        assert(json_data.get('id') != None)
        utils.removeFromActiveClient(ACTIVE_CLIENTS , vm_name , json_data.get('id'))
    except:
        return "error: "+sys.exc_info() , 400
    
    monitoring_details = CACHE.getCachedJsonWithRetry(json_data['id'], 5)
    if(monitoring_details is None):
        return "Given Id not found in Server Cache", 404
    if(monitoring_details['action'] == 'START_MONITORING' and monitoring_details['status'] == 'OK' and monitoring_details["payload"]["monitoring_pId"] is not None): ##{'id': 'c840d363-ec6f-4cbf-96f4-de2d903a6563', 'action': 'START_MONITORING', 'status': 'OK', 'payload': {'monitoring_pId': None}, 'parameters': {'process_name': 'chrome', 'polling_interval': 60, 'latest': True}}
        msg = dict(message_frame)
        msg["action"] = "STOP_MONITORING"
        msg["id"]= json_data['id']
        msg["params"]= monitoring_details
        socketio.emit(vm_name , json.dumps(msg))
        return jsonify({
            "id":json_data['id'],
            "data_url":"/datastore/"+json_data['id']
        })
    else:
        return jsonify({
            "id":json_data['id'],
            "msg":"Pre-requesite evaluation Failed: " + json.dumps(monitoring_details)
        }), 500

@app.route('/api/<id>/stats', methods=['GET'])
def getStats(id):
    fileName = path.join(CONFIG.datastore , id+'.json')
    if(not path.exists(fileName)):
        return "given id: {0} is not found".format(id), 404
    return jsonify( utils.getStats(fileName) )


"""
{
    "start_frequency":10,
    "end_frequency":10,
    "difference_limit":5
}
Validates that the avg memory for last 10 minutes ( intervals ) is less than or equal to 5x the avg memory during the first 10 minutes
"""
@app.route("/api/<id>/validate", methods = ['POST'])
def valdiate(id):
    fileName = path.join(CONFIG.datastore , id+'.json')
    if(not path.exists(fileName)):
        return "given id: {0} is not found".format(id), 404
    req_body = request.get_json()
    start_frequency = req_body["start_frequency"]
    end_frequency = req_body["end_frequency"]
    diffrence_limit = req_body["difference_limit"]
    startAvg = utils.get_avg_of_N_entries(fileName , start_frequency )
    endAvg = utils.get_avg_of_N_entries(fileName , end_frequency , False)
    result = startAvg * diffrence_limit > endAvg
    return jsonify({
        "avg_start_memory":startAvg,
        "avg_end_memory":endAvg,
        "validationStatus": str(result)
    })



@app.route('/sendcustomEvent', methods=['GET'])
def sendnew():
    q = request.args.get('event')
    msg = request.args.get('msg')
    socketio.emit(q, msg)
    return "OK"


@app.route('/sendcustomEventPOST', methods=['POST'])
def sendnewPOST():
    data = request.get_json()
    topic = data['topic']
    msg = data['msg']
    socketio.emit(topic, msg)
    return "OK"

@app.route('/datastore/<id>', methods=['GET','POST'])
def datastore(id):
    if(request.method == 'GET'):
        fileName = path.join(CONFIG.datastore , id+'.json')
        if(path.exists(fileName)):
            return jsonify(json.load(open(fileName)))
        else:
            return "file not found",404
    json_data = request.get_json()
    fileName = path.join(CONFIG.datastore , id+'.json')
    json.dump(json_data , open(fileName , 'w+'))
    return 'OK',200

@app.route('/ui/datastore/<id>', methods=['GET'])
def datastoreUI(id):
    fileName = path.join(CONFIG.datastore , id+'.json')
    if(path.exists(fileName)):
        js = json.load(open(fileName))    
    else:
        return "file not found",404
    return render_template('Result.html',tool_name="{0} | {1}".format(js["hostname"] ,js["process_name"]),tm_data=js["memory_usage"])


@app.route('/ui/activeclients', methods = ['GET'])
def showActiveClients():
    return jsonify(ACTIVE_CLIENTS)
###### Socket IO events

@socketio.on('connection_information')
def doOnConnect(data):
    if(utils.getIndexOfObject(ACTIVE_CLIENTS,'hostName', data['hostName']) == -1):
        ACTIVE_CLIENTS.append(data)
    print("Some One connected")

@socketio.on('disconnect')
def doOnDisconnect():
    print("Someone disconnected!")
#######


if __name__ == '__main__':
    socketio.run(app,  host=CONFIG.bind_host, port=CONFIG.bind_port)
