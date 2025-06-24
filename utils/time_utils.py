from datetime import datetime, timedelta
from pytz import timezone

def get_current_date():
    return datetime.now(timezone('utc')).strftime('%Y-%m-%d')

def get_current_time():
    return datetime.now(timezone('utc')).strftime('%H-%M-%S')

def get_previous_date():
    yesterday = datetime.now(timezone('utc')) - timedelta(1)
    return yesterday.strftime('%Y-%m-%d')