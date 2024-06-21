import socket
from urllib.request import urlopen
import requests
import json
import platform
import subprocess
from datetime import datetime
import psutil
import ctypes
import os
import time

def get_ip_info(ip):
    try:
        request_url = f'https://geolocation-db.com/jsonp/{ip}'
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        return json.loads(result)
    except Exception:
        return {
            'country_name': 'Unknown',
            'city': 'Unknown',
            'latitude': 'Unknown',
            'longitude': 'Unknown',
            'state': 'Unknown'
        }

def get_info():
    info = {}
    try:
        info['ip'] = urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8').strip()
        ip_info = get_ip_info(info['ip'])
        info['country'] = ip_info['country_name']
        info['city'] = ip_info['city']
        info['latitude'] = ip_info['latitude']
        info['longitude'] = ip_info['longitude']
        info['state'] = ip_info['state']
    except Exception:
        info['ip'] = 'Unknown'
        info['country'] = 'Unknown'
        info['city'] = 'Unknown'
        info['latitude'] = 'Unknown'
        info['longitude'] = 'Unknown'
        info['state'] = 'Unknown'
    

    try:
        uname = platform.uname()
        info['system'] = uname.system
        info['host_name'] = uname.node
        info['release'] = uname.release
        info['version'] = uname.version
        info['machine'] = uname.machine
        info['processor'] = uname.processor
    except Exception:
        info['system'] = 'Unknown'
        info['host_name'] = 'Unknown'
        info['release'] = 'Unknown'
        info['version'] = 'Unknown'
        info['machine'] = 'Unknown'
        info['processor'] = 'Unknown'
    
    try:
        info['is_admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        info['is_admin'] = 'Unknown'
    
    try:
        info['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        info['start_time'] = 'Unknown'
    
    try:
        info['microphones'] = get_microphone_count()
    except Exception:
        info['microphones'] = 'Unknown'
    
    try:
        webcams = get_video_devices()
        info['webcams'] = len(webcams) if webcams != 'Unknown' else 'Unknown'
    except Exception:
        info['webcams'] = 'Unknown'
    
    try:
        monitors = get_monitors()
        info['monitors'] = len(monitors) if monitors != 'Unknown' else 'Unknown'
    except Exception:
        info['monitors'] = 'Unknown'
    
    try:
        info['cpu'] = get_cpu_info()
    except Exception:
        info['cpu'] = 'Unknown'
    
    try:
        info['gpu'] = get_gpu_info()
    except Exception:
        info['gpu'] = 'Unknown'
    
    try:
        info['ram'] = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
    except Exception:
        info['ram'] = 'Unknown'
    
    try:
        info['install_date'] = get_install_date()
    except Exception:
        info['install_date'] = 'Unknown'
    
    return info

def get_microphone_count():
    try:
        result = subprocess.check_output(
            'powershell "Get-PnpDevice -Class AudioEndpoint | Select-Object -Property FriendlyName"', 
            shell=True
        ).decode()
        devices = result.split("\n")[3:-1]
        microphones = set()
        for device in devices:
            device_name = device.strip()
            if "Microphone" in device_name and "High Definition Audio" not in device_name:
                microphones.add(device_name)
        return len(microphones)
    except Exception:
        return 'Unknown'

def get_video_devices():
    try:
        result = subprocess.check_output(
            'powershell "Get-WmiObject Win32_PnPEntity | Where-Object { $_.Service -eq \'usbvideo\' } | Select-Object -Property Name"', 
            shell=True
        ).decode()
        devices = result.split("\n")[3:-1]
        return [device.strip() for device in devices if device.strip()]
    except Exception:
        return 'Unknown'

def get_monitors():
    try:
        from screeninfo import get_monitors
        return [str(monitor) for monitor in get_monitors()]
    except Exception:
        return 'Unknown'

def get_cpu_info():
    try:
        result = subprocess.check_output('wmic cpu get name', shell=True).decode()
        cpu_info = result.split("\n")[1].strip()
        return cpu_info
    except Exception:
        return 'Unknown'

def get_gpu_info():
    try:
        result = subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode()
        devices = result.split("\n")[1:-1]
        return [device.strip() for device in devices if device.strip()]
    except Exception:
        return 'Unknown'

def get_install_date():
    try:
        file_creation_time = os.path.getctime(__file__)
        install_date = datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d %H:%M:%S')
        return install_date
    except Exception:
        return 'Unknown'

def main():
    info = get_info()
    formatted_info = (
        f"Start Time: {info['start_time']}\n"
        f"Elevated permissions: {info['is_admin']}\n"
        f"IP: {info['ip']}\n"
        f"Country: {info['country']}\n"
        f"City: {info['city']}\n"
        f"Latitude: {info['latitude']}\n"
        f"Longitude: {info['longitude']}\n"
        f"State: {info['state']}\n"
        f"Host Name: {info['host_name']}\n"
        f"OS: Windows {info['release']}\n"
        f"Microphones: {info['microphones']}\n"
        f"Webcams: {info['webcams']}\n"
        f"Monitors: {info['monitors']}\n"
        f"CPU: {info['cpu']}\n"
        f"GPU: {', '.join(info['gpu']) if isinstance(info['gpu'], list) else info['gpu']}\n"
        f"RAM: {info['ram']}\n"
        f"Install Date: {info['install_date']}\n"
    )
    print(formatted_info)

main()
