import json
import re
import subprocess
from terminaltables import SingleTable
from colorclass import Color, Windows
from os import system, name, path
import requests
import psutil
from collections import namedtuple  
from subprocess import Popen
import logging
import sys
import requests
import configuration
import os

CONFIG = configuration.CONFIG

def clear():  
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_status(hostname , server_name , status ):
    clear()
    if('fail' in status.lower()):
        msg = [Color('{autored}Status'), status]
    else:
        msg = [Color('{autogreen}Status'), status]

    table_data = [
        [Color('{autogreen}Client'), hostname],
        msg,
        [Color('{autoyellow}Server'), server_name]
    ]
    table_instance = SingleTable(table_data)
    table_instance.inner_heading_row_border = False
    return table_instance.table


def getProcess_list():
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
        # Get process detail as dictionary
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        # Append dict of process detail in list
        listOfProcessNames.append(pInfoDict)
    return listOfProcessNames

def get_pid(process_name, latest = True):
    pids=[]
    for proc in psutil.process_iter():
        try:
            if(process_name in proc.name()):
                pids.append(proc.pid)
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if(pids.__len__()==0):
        return -1 # return -1 if a process is not found
    elif(latest):
        return pids[-1]
    return pids[0]



def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())


def start_monitoring(process_id , id , polling_interval):
    CONFIG = json.load(open('client_config.json'))
    if(CONFIG['mode']=='exe'):
        cmd_str = 'memory_monitoring_thread.exe -p {0} -i {1} -d {2} -t {3}'.format(process_id , id , CONFIG['memory_log_directory'], polling_interval)
    else:
        cmd_str = 'python memory_monitoring_thread.py -p {0} -i {1} -d {2} -t {3}'.format(process_id, id , CONFIG['memory_log_directory'] ,polling_interval )   
    
    logging.info("Executing Command : "+ str(cmd_str) )
    try:
        # proc = subprocess.Popen(cmd_str, shell=True,
        #         stdin=None, stdout=None, stderr=None, close_fds=True ,cwd= path.dirname(path.abspath(__file__)))
        logging.info("Sub Process HandOvercommand: "+ cmd_str)
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        logging.info("Process started successfully .."+ str(proc.pid))
    except Exception as e :
        logging.error("Error Occurred "+ str(e))
        raise e
    return proc.pid

def kill_process(pid):
    try:
        process = psutil.Process(int(pid))
    except:
        logging.error("Unable to find processId {0} to terminate ".format(str(pid)))
    process.terminate()
    return 0

def persist_to_server(id, url ):
    file_path = path.join(CONFIG.memory_log_directory , id+'.json')
    if(path.exists(file_path)):
        payload_data = json.load(open(file_path,'r'))
        response = requests.post(url , json= payload_data)
        if(response.status_code==200):
            return True
        else:
            logging.error("Server Error: response code: " +  response.status_code)
            raise Exception("Server Error: response code: " +  response.status_code)
    else:
        logging.error("Unable to find the given file: "+ file_path )
        raise Exception("Unable to find memory Snapshot on client")