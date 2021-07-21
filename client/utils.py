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
        if(process_name in proc.name()):
            pids.append(proc.pid)
    if(pids.__len__()==0):
        return -1 # return -1 if a process is not found
    elif(latest):
        return pids[-1]
    return pids[0]



def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())


def start_monitoring(process_id , id , polling_interval):
    CONFIG = json.load(open('client_config.json'))
    # cmd_str=[
    #     "python",
    #     "memory_monitoring_thread.py",
    #     "-p",
    #     str(process_id),
    #     "-i",
    #     id,
    #     "-d",
    #     CONFIG['memory_log_directory'],
    #     "-t",
    #     str(polling_interval)
    # ]
    cmd_str = 'python memory_monitoring_thread.py -p {0} -i {1} -d {2} -t {3}'.format(process_id, id , CONFIG['memory_log_directory'] ,polling_interval )
    
    logging.info("Executing Command : "+ str(cmd_str) )
    try:
        proc = subprocess.Popen(cmd_str, shell=True,
                stdin=None, stdout=None, stderr=None, close_fds=True ,cwd= path.dirname(path.abspath(__file__)))
        logging.info("Process started successfully .."+ str(proc.pid))
    except Exception as e :
        logging.error("Error Occurred "+ str(e))
        raise e
    return proc.pid