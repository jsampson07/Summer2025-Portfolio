# Async Port Scanner

**A high-performance asynchronous TCP port scanner built with Python**

This project demonstrates the use of Python's 'asyncio' library to perform non-blocking, concurrent TCP port scanning. It's designed to efficiently identify open ports on a target host, making it a valuable tool for network administrators and cybersecurity enthusiasts.

---

## Features

- **Asynchronous Scanning**: Utilizes 'asyncio' to scan multiple ports concurrently, significantly reducing scan time compared to traditional methods.
- **Customizable Port Range**: Allows users to specify a range of ports to scan (for now within a predefined set of ports).
- **Simple Command-Line Interface**: Easy to use with basic command-line arguments for quick scans.

---

## Tech Stack

- **Programming Language**: Python 3
- **Libraries**: 'asyncio', 'socket'
- **Protocols**: TCP/IP

---

## Current Status

This project is in active development. The core functionality for asynchronous port scanning is implemented, but additional features such as service identification, output formatting, and improved error handling are planned for future updates.

---

## Setup Instructions
```bash
#Clone the repository
git clone https://github.com/yourusername/async-port-scanner.git

#Run the scanner
python3 port_scanner_async.py -s <subnet> -p <ports> -t <timeout> -v <verbose level> -c <num_concurrent tasks>
  - note: <subnet> is the only required field
