# Netnucleus

A Simple Web application for managing a classroom environment

## Introduction

NetNucleus is designed for educators and administrators who 
need an efficient way to manage a classrooms computer software, and shutdown schedules. 
This repository provides both the client application
and a set of service automation tools.

## Features

- **User-friendly interface:** Easy management of classroom activities.
- **Shutdown Computers:** Ability to shutdown computers from a remote location.
- **Install Software and Updates:** Either to all computers or a chosen device.
- **Device Statistics:** View the storage, Firewall Status, Bitlocker Status, and Logged in user for a device.
  

## Getting Started

### Prerequisites

 ```bash
 git clone https://github.com/Plananas/NetNucleus.git
 ```

#### **On Site Server**
- Docker Engine
- Windows Professional, Education, Server, Enterprise
<br /> **OR**
- Python 3.10 
- Python packages listed in requirements.txt

#### **Client Application**
- Python 3.10
- Python packages listed in requirements.txt
- Scoop
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

#### **Overseer Server**
- Docker Engine
- Windows Professional, Education, Server, Enterprise
<br /> **OR**
- Python 3.10
- Python packages listed in requirements.txt

---

### Installation

#### **On Site Server**

1. **Open Directory:**
 ```bash
 cd NetNucleus/ClientApplication
 ```

3. **Open Docker Engine**
Run the docker engine for windows containers

4. **Run the Docker Box**  
```bash
docker compose up --build
```

4. **Add Address to hosts file**
```bash
./addHosts.sh
```

---

#### **Client Application**

1. **Open Directory:** 
 ```bash
 cd NetNucleus/ClientApplication
 ```

2. **Set the server IP Address:** 
Add a value to the line `SERVER_ADDRESS` in the .env file

3. **Run the Python File:** 
You can either run it directly through python as a terminal application (good for testing purposes) <br />
Or you can run it as a windows service, it will run in the background and be available to run on startup <br />

**Python Terminal App**
```bash
python ClientApp.py
```
**Windows Service**
```bash
python NetworkAutomationService.py install
python NetworkAutomationService.py start
```
**Remove/Stop Windows Service**
```bash
python NetworkAutomationService.py stop
python NetworkAutomationService.py remove
```
---

#### **Overseer**

1. **Open Directory:**
 ```bash
 cd NetNucleus/Overseer
 ```

3. **Open Docker Engine**
Run the docker engine for windows containers

4. **Run the Docker Box**  
```bash
docker compose up --build
```

4. **Add Address to hosts file**
```bash
./addHosts.sh
```

---
## Terminal Application
The terminal commands can only be ran on the server hosting this application.

### Commands

| Command                                 | Description                                                                 |
|-----------------------------------------|-----------------------------------------------------------------------------|
| `shutdown`                              | Shuts down all connected client machines.                                  |
| `shutdown <client_id>`                  | Shuts down the specified client by UUID.                                   |
| `install <software> <client_id>`        | Installs the specified software on the given client machine.               |
| `install <software>`                    | Installs the specified software on all connected clients.                  |
| `upgrade <software> <client_id>`        | Upgrades the specified software on the given client machine.               |
| `upgrades <client_id>`                  | Upgrades all upgradable software on the given client machine.              |
| `software <client_id>`                  | Displays a list of installed software on the specified client in JSON.     |
| `uninstall <software> <client_id>`      | Uninstalls the specified software from the given client machine.           |
| `createuser <username>:<password>`      | Creates a new user account with the given credentials.                     |

---
## API
The set of REST endpoints available in the application. 
### Endpoints
| Endpoint                      | Method | Description                                                                 |
|------------------------------|--------|-----------------------------------------------------------------------------|
| `/api/clients/shutdown`      | POST   | Shuts down all clients, or a specific list if `clients` array is provided. |
| `/api/clients/install`       | POST   | Installs the specified software on a client. Requires `software` and `uuid`.|
| `/api/clients/uninstall`     | POST   | Uninstalls the specified software from a client. Requires `software` and `uuid`.|
| `/api/clients/upgrade`       | POST   | Upgrades specified software on a given client. Requires `software` and `uuid`.|
| `/api/clients/upgrades`      | POST   | Without a body: upgrades all software on all clients. With UUID: upgrades software on one.|
| `/api/clients/software`      | POST   | Returns installed software on a client in JSON. Requires `uuid`.            |

---


## Future Updates

- **Automation Rules:** Set timed update scans/ shutdowns
- **Default Applications:"" Customizable application list to be downloaded on new devices


