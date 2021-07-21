import re
from terminaltables import SingleTable
from colorclass import Color, Windows
from os import system, name
import requests
import psutil
from collections import namedtuple  

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


def customJsonDecoder(dictVar):
    return namedtuple('X', dictVar.keys())(*dictVar.values())