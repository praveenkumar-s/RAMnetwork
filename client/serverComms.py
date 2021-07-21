import json
import re
from flask.globals import request
import requests
import urllib.parse
import logging
import sys

class ServerCommunication():
    def __init__(self, host , port=80 ):
        self.host = host
        self.port = port
        self.url = 'http://{host}:{port}/'.format(host=host,port=port)
    
    def send_frame(self,id,frame):
        url = urllib.parse.urljoin(self.url , '/api/save/{id}'.format(id=id))
        rs = requests.post(url = url , json = frame)
        if(rs.status_code==200):
            logging.info("Submitted Payload {id} to server Successfully ".format(id = id))
            return True
        else:
            logging.error("Error while sending Payload to server " + sys.exc_info() )
            return False