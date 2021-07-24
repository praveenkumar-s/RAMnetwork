# Distributed Memory monitoring
Start and stop logging memory used by a specific process(s) on a remote machine by interacting with a central API. Handy tool to monitor Apps for Memory Leaks

##### Note: 🚨 🚧 🚧 This project is work in progress 🚧 🚧 🚨

### Uses:
* In a multi processing distributed system, tracking process memory on each machine / node can be hard 
* Turbocharge your CI/CD pipelines to start monitoring memory used by your jobs and actions
* Store memory trends on a central location and visualize them using a web-ui

## Installation and Usage:

## Server:
    Copy the contents of the server folder to a local machine. 
#### Docker: 
    docker build -t memoryMonitorServer . 
    docker run -d --name memoryMonitorServer -p 5001:5001 memoryMonitorServer

#### Metal:
    python -m pip install -r requirements.txt
    python app.py

### Server Configurations:
Server side configurations are controlled by `server_config.json`
```
{
    "bind_host":"0.0.0.0",         --> IP address to bind on 
    "bind_port":5001,              --> Port Number to Bind to 
    "redis_cache":{
        "server":"192.168.88.219", ---> IP Address of redis service  
        "port":6379                ----> Port number of Redis service 
    } ,
    "datastore": "datastore"       ----> Local directory on server where the incomming memory logs from clients will be saved
}
```

Redis server installation and configuration can be found at : https://docs.redislabs.com/latest/rc/

### API Documentation: 
    https://documenter.getpostman.com/view/1523598/TzsZqnq4


## Client
Clients are executables that are always running on the nodes that we want to track. The client must be installed to start on start-up of system

### Portable Installation (Windows):
Copy the Contents of /client_windows_x86 in to a local folder and start client by : `memClient.exe`

### Universal Install ( Windows / Linux / Unix ):
Copy the contents of `client` folder in to a local directory
`python -m pip install -r requirements.txt`
`python memClient.py`

### Client startup: 
![Alt text](documentation/clientStartup.png?raw=true "Client Startup ")

### Client configurations:
```
{
    "server_ip":"192.168.88.219",      --> IP of the Memory Monitoring Server
    "server_port":5001,                --> Port number of Server
    "memory_log_directory":"datastore" --> Local directory where memory snapshots would be stored
}
```


### WebUI
The Web UI for visualizing a memory snapshot: 
`http://hostname:port/ui/datastore/<id of snapshot>`

To view a demo visualization: `http://hostname:port/ui/datastore/demo`

### Client startup: 
![Alt text](documentation/DemoImage.png?raw=true "Client WebUI Demo Image ")