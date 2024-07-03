# Raspberry Pi Temperature Monitor

This project is designed to monitor the CPU temperatures of multiple Raspberry Pis and display the data on an Arduino LCD. Additionally, it monitors room temperature and humidity using a DHT sensor connected to the Arduino. The script reads local and remote temperatures and sends the data via serial communication to an Arduino, which then displays the temperature and humidity information.

## Features

- Reads CPU temperature from multiple Raspberry Pis using SSH
- Displays temperature data on an Arduino LCD
- Monitors room temperature and humidity using a DHT sensor connected to the Arduino
- Configurable via a JSON configuration file

## Requirements

- Python 3
- Paramiko library
- pySerial library
- An Arduino with an LCD display and DHT sensor (e.g., DHT11)
- Multiple Raspberry Pis

## Installation

1. **Clone the Repository**

- git clone https://github.com/gessnerda/rpiTemps.git
- cd rpiTemps

2. **Install libraries**

- pip install paramiko pyserial

3. **Create and fill in config.json**

- cp config_template.json config.json

4. **Run**

- python .\rpiTemps