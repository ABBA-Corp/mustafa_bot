import datetime
from datetime import date

def check_data():
    now = datetime.datetime.now()
    if now.weekday() == 3 and  now.hour >= 18 or now.weekday() == 4 and  now.hour <= 18:
        return print(True)
    else:
        return print(False)

check_data()