#<imports>
import datetime
import json
import os
#</imports>

def force_decode(b: bytes):
    try:
        return b.decode(json.detect_encoding(b))
    except UnicodeDecodeError:
        return b.decode(errors="backslashreplace")
    
def current_time(with_seconds=False):
    return datetime.datetime.now().strftime('%d.%m.%Y_%H.%M' if not with_seconds else '%d.%m.%Y_%H.%M.%S')

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def implode():
    pass