import datetime
from dateutil import tz # pip install python-dateutil
# https://stackoverflow.com/questions/12145847/using-python-what-is-the-most-accurate-way-to-auto-determine-a-users-current-ti

def convert_utc_datetime(utc): #, tz=tz.tzlocal()p
    return datetime.datetime.fromtimestamp(utc).strftime('%m/%d/%Y(%a)%H:%M:%S')

def convert_utc_datetime2(utc):
    import time
    from datetime import datetime

    import pytz # $ pip install pytz
    from tzlocal import get_localzone # $ pip install tzlocal

    # get local timezone
    local_tz = get_localzone()

    # test it
    # utc_now, now = datetime.utcnow(), datetime.now()
    #ts = time.time()
    ts = utc
    utc_now, now = datetime.utcfromtimestamp(ts), datetime.fromtimestamp(ts)

    local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz) # utc -> local
    assert local_now.replace(tzinfo=None) == now

    return local_now