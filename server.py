import serial
import time
import paramiko 
import subprocess 
import json
import os

config_path = 'config.json'

if not os.path.exists(config_path):
    print(f"Configuration file '{config_path}' not found. Please create it based on 'config_template.json'.")
    exit(1)

with open(config_path) as config_file:
    config = json.load(config_file)

serial_port = config['serial_port']
raspberry_pis = config['pis']

def get_cpu_temp_from_pi(pi_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(pi_ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command("vcgencmd measure_temp")
        temp_str = stdout.read().decode().strip()
        client.close()
        
        # Debug information
        print(f"CPU temperature string from {pi_ip}: '{temp_str}'")
        
        return float(temp_str.split('=')[1].split('\'')[0])
    except Exception as e:
        print(f"Error getting CPU temperature from {pi_ip}: {e}")
        return None

def get_cpu_temp_local():
    try:
        temp_str = subprocess.check_output(["vcgencmd", "measure_temp"]).decode().strip()
        print(f"Local CPU temperature string: '{temp_str}'") 
        return float(temp_str.split('=')[1].split('\'')[0])
    except Exception as e:
        print(f"Error getting local CPU temperature: {e}")
        return None

def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

ser = serial.Serial(serial_port, 9600)

while True:
    #had to do this bc the ordering in displaying was wrong smh
    devpi_temp = get_cpu_temp_from_pi(raspberry_pis[0]["ip"], raspberry_pis[0]["username"], raspberry_pis[0]["password"])
    if devpi_temp is not None:
        ser.write(f"0:{celsius_to_fahrenheit(devpi_temp)}\n".encode())
    time.sleep(2)
    
    local_temp = get_cpu_temp_local()
    if local_temp is not None:
        ser.write(f"1:{celsius_to_fahrenheit(local_temp)}\n".encode())
    time.sleep(2)

    for i, pi in enumerate(raspberry_pis[1:], start=2):
        cpu_temp = get_cpu_temp_from_pi(pi["ip"], pi["username"], pi["password"])
        if cpu_temp is not None:
            ser.write(f"{i}:{celsius_to_fahrenheit(cpu_temp)}\n".encode())
        time.sleep(2)
