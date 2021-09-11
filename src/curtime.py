from datetime import datetime


def curtime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
