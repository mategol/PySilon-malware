import datetime

def current_time():
    return datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
