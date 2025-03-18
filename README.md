# py_talk Documentation v0.0.0

py_talk is a lightweight Python-based system designed to enhance the safety of automated downloads by acting as a **disposable firewall**. It is currently implemented for **local machines** and serves as an intermediary for processing common 3D printing files (such as **STL and OBJ**) before allowing them to reach more sensitive production environments. By isolating downloads and performing security checks, py_talk aims to **prevent malware infections from spreading**.

---
## Overview

In automated workflows—specificaly those involving **3D printing files**—maintaining system integrity is crucial to contunuous operation.

py_talk provides an **extra layer of protection** by:
- Allowing a **disposable system** to process unverified files before moving them to a more secure environment.
- Preventing **direct exposure** of sensitive systems to files from untrusted sources.
- Enabling a **two-stage processing approach**, allowing faster uploads that can be processed later without security risks.

This **isolated processing model** was inspired by security structures used by large corporations, where subsystems are **compartmentalized** to prevent infections from spreading.

## ***This is not a replacement to anti malware and other forms of cyber attacks, but rather a check for specific file types that will be processed often***

<br></br>
> **NOTE:** This project is still in progress, and not all features are publicly available.

---
## Scanning for Malware

The server performs the following security tasks:

- **File Type Verification:** Ensures files match expected formats (e.g., STL, OBJ).
- **Malware Scanning:** Uses **ClamAV** to detect infected files.
- **Isolation on Detection:** If a file is flagged as malicious, it is moved to a **JAIL** directory, and an **email warning** is triggered.
- **Security Status Monitoring:** If a system-wide infection is detected, the server will **shut down** or set `GET /status` to `{ "secure": false }`.
- **Intermediary Processing:** Only verified files can be downloaded and processed, preventing direct exposure of sensitive systems.



---
# Why was py_talk created?

### ✅ Enhanced Security
Acts as a **disposable firewall** to prevent malware from reaching sensitive systems.

### 🔍 Automated Safety Checks
Scans files for **malware** and verifies common **3D printing formats** that get processed often in the context of 3d printing.

### 🔒 Secure File Handling
Uses **SSH/SFTP** for secure file downloads and **logging** for troubleshooting.

### 🚀 Future-Ready Architecture
Currently built for **local machines**, but designed to support **decentralized systems** in the future.

---
# Features

## 📡 REST API Server

### **GET /scanned**
Returns a **JSON list** of scanned files, excluding system directories like `DONE` or `JAIL`.

### **POST /scanned**
Accepts a JSON payload to remove specific files from the scanned list and move them to the **DONE** directory.

### **GET /status**
Returns the server's **security status**:
- ✅ **Normal:** `{ "secure": true }`
- ❌ **Infected:** `{ "secure": false }` (or no response if the server is shut down)

---

## 🖥️ Client Operations
The `py_talk` class in `client.py` provides methods to:
- Retrieve **scanned files** from the server.
- Remove processed files (moving them to the **DONE** directory).
- Download **verified files** securely via **SSH/SFTP**.

---
## 🔍 Security Checks & Isolation

- **Malware & File Type Verification:** Ensures all files are clean and match expected **3D printing formats**.
- **Quarantine on Threat Detection:** Infected files are **moved to JAIL**, and an **email notification** is sent to administrators.
- **Infection Handling:** If a severe infection is detected, the server will either **shut down** or update its **security status**.

**for more informaton on how files are verified** check out [3D File Verification Repository](https://github.com/MarsTheProtogen/3d_file_verification).
it is the libary the file scanning is based off of.

---

# Current Implementation

### 🔹 Local Machine Deployment
The system is designed for **local network use**, where both server and client components run within the same environment.

### 🔹 3D Printing File Support
Supports **STL and OBJ** formats, ensuring only verified files reach production systems.

### 🔹 Disposable Firewall System
Acts as an **isolated pre-processing stage**, preventing **direct exposure** of sensitive machines to external files.

---

# Future Improvements

### 🔜 **Additional Security Checks**
- Additional **malware scanning** capabilities.
- **File integrity verification** improvements.

### 🔜 **Email Notifications**
- Real-time **alerts** for malware detection and security events.

### 🔜 **Decentralized System Support**
- Expanding support for **remote and distributed environments**.

### ❌ **No Web Dashboard Planned**
- Currently focused on **backend security**; no **web UI** planned.

---

# Installation & Setup

## 📥 Clone the Repository
```sh
git clone https://github.com/MarsTheProtogen/py_talk.git
cd py_talk
```

## 📦 Install Dependencies
Ensure Python 3.x is installed and run:
```sh
pip install flask requests paramiko
```

## 🚀 Server Setup
```sh
mkdir -p SCANNED/DONE SCANNED/JAIL
python server.py
```

## 🖥️ Client Setup
Create a `settings.json` file:
```json
{
  "host": "your.server.address",
  "port": 22,
  "username": "your_username",
  "key": "path/to/your/rsa_key.pem",
  "SYNC_DIR": "/path/on/server/to/sync",
  "DOWNLOAD_DIR": "/path/on/client/to/download"
}
```
Run the client:
```sh
python client.py
```

---

# Usage

## 📡 Server API Endpoints

### **GET /scanned**
Returns scanned files **excluding** `DONE` and `JAIL`.

### **POST /scanned**
Removes files from the scanned list:
```json
{"remove": ["filename1.stl", "filename2.obj"]}
```

### **GET /status**
- ✅ **Normal:** `{ "secure": true }`
- ❌ **Infected:** `{ "secure": false }`

## 🖥️ Client Methods

### **get_scanned_files()**
Retrieves the list of **scanned files**.

### **remove_scanned_file(filename)**
Removes a **specific file** from the scanned list, moving it to **DONE**.

### **download_scanned_file(files: list)**
Securely **downloads files** from the server using **SSH/SFTP**.

---

# Code Structure Overview

### 📡 **server.py**
Handles:
- Oops! The code took a coffee break
<!--- **Flask API** for file scanning and management.
- **Malware and file type verification**.
- **Moving infected files to JAIL & sending alerts**.
- **Updating security status via GET /status**.-->

### 🖥️ **client.py**
Handles:
- perhaps the human did too... 
<!--- **Fetching, removing, and downloading** scanned files.
- **Secure SSH/SFTP file transfers**.-->

---

🚀 **py_talk** is designed to **securely handle automated downloads** while protecting sensitive systems. Future updates will enhance **security, decentralization, and automation.**

---

<br></br>

<br></br>

<br></br>

<br></br>

<br></br>
