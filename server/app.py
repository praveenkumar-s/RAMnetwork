import json
from os import confstr, name, environ
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
    id = str(uuid4())
    msg = dict(message_frame)
    msg["action"] = "GET_PROCESS_LIST"
    msg['id'] = id
    socketio.emit(vm_name, json.dumps(msg))
    process_list = CACHE.getCachedJsonWithRetry(id, 10)
    return jsonify(process_list)


@app.route('/api/save/<id>', methods=['POST'])
def saveResponse(id):
    json_data = request.get_json()
    CACHE.setCacheJson(id, json_data)
    return 'OK', 200

@app.route('/api/<vm_name>/startMonitoring',methods=['POST'])
def startMonitoring(vm_name):
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
    return jsonify({
        "id":id,
        "status": response['status'],
        "payload": response['payload']  
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


if __name__ == '__main__':
    socketio.run(app,  host=CONFIG.bind_host, port=CONFIG.bind_port)
