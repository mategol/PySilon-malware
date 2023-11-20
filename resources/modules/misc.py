import datetime
import json

def force_decode(b: bytes):
    try:
        return b.decode(json.detect_encoding(b))
    except UnicodeDecodeError:
        return b.decode(errors="backslashreplace")
    
def current_time(with_seconds=False):
    return datetime.datetime.now().strftime('%d.%m.%Y_%H.%M' if not with_seconds else '%d.%m.%Y_%H.%M.%S')