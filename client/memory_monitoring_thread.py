# args: processID , refID , data_storage_path
import argparse
import os
import psutil
import time
from datetime import date, datetime, timedelta
import json





if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-p", "--processId", required=True,
    help="ProcessId of the process to be monitored ")
    ap.add_argument("-i", "--refId", required=True,
    help="Server generated request Id")
    ap.add_argument("-d", "--outputDir", required=True,
    help="Directory to store the output file")
    ap.add_argument("-t", "--timeInterval", required=False,
    help="Polling interval for monitoring")
    args = vars(ap.parse_args())

    processId = args.get('processId')
    id = args.get('refId')
    outputDirectory = args.get('outputDir')
    pollingInterval = int(args.get("timeInterval",60))
    file_name = os.path.join(outputDirectory,id+'.json')
    memory_footPrint = []
    last_updated_time = None
    try:
        process = psutil.Process(int(processId))
        json.dump(memory_footPrint , open(file_name , 'w+'))
        last_updated_time = datetime.utcnow()
    except:
        json.dump(memory_footPrint , open(file_name , 'w+'))
        exit()
    
    while True:
        try:
            memory_usage = process.memory_info()
            memory_footPrint.append([datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S") , memory_usage[0]])
        except:
            json.dump(memory_footPrint , open(file_name , 'w+'))
            exit()
        finally:
            if((datetime.utcnow()-last_updated_time).total_seconds() > 30):
                json.dump(memory_footPrint , open(file_name , 'w+'))
                last_updated_time = datetime.utcnow()
        time.sleep(pollingInterval)
        


