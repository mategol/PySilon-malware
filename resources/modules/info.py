from urllib.request import urlopen
import requests
import json
import os
import platform

def get_info():
    info = {}
    info['ip'] = urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8')
    
    request_url = 'https://geolocation-db.com/jsonp/' + info['ip']
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    info['country'] = json.loads(result)['country_name']
    
    print(platform.uname())





get_info()







# Started at
# Elevated permissions
# IP
# Country
# City
# Hostname
# OS
# Microphone
# Webcam
# Monitors
# Antivirus
# CPU
# GPU
# RAM
# Installed at
# 
# 
# 