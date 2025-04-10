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
OR
- Python 3.10 
- Python packages listed in requirements.txt

#### **Client Application**
- Python 3.10
- Python packages listed in requirements.txt

#### **Overseer Server**
- Docker Engine
- Windows Professional, Education, Server, Enterprise
OR
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

1. **Open Directory**
 ```bash
 cd NetNucleus/ClientApplication
 ```

2. **Set the server IP Address**
Add a value to the line `SERVER_ADDRESS` in the .env file

3. **Run the Python File**
```bash
python ClientApp.py
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

## Future Updates

- **Automation Rules:** Set timed update scans/ shutdowns


