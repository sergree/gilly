import datetime


def current_time():
    return str(datetime.datetime.now()) + ': '


def log(*msg):
    print(current_time() + ' '.join([str(x) for x in msg]))
