from datetime import datetime
from pytz import timezone

def get_current_date():
    return datetime.now(timezone('utc')).strftime('%Y-%m-%d')

def get_current_time():
    return datetime.now(timezone('utc')).strftime('%H-%M-%S')