import requests
import datetime as dt
from functools import wraps
import pytz
import numbers

__title__ = "ginlong"
__version__ = "0.0.1"
__author__ = "Aleksander Lyse"
__license__ = "MIT"

URLS = {
    'baseUrl': 'http://apic-cdn.solarman.cn/v/ap.2.0'
}


def authenticated(func):
    """
    Decorator to check if Smappee's access token has expired.
    If it has, use the refresh token to request a new access token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.refresh_token is not None and \
           self.token_expiration_time <= dt.datetime.utcnow():
            self.re_authenticate()
        return func(*args, **kwargs)
    return wrapper


class Ginlong(object):

    def __init__(self):
        
        self.username = None
        self.password = None
        self.user_id = None

        self.access_token = None



    def authenticate(self, username, password):

        url = urljoin(URLS['baseUrl'], '/cust/user/login')
        params = {

            "user_id": username,
            "user_pass": password
        }
        r = requests.get(url, params=params )
        r.raise_for_status()
        j = r.json()
        self.access_token = j['token']
        self.user_id = j['uid']
        return r


    def get_powerplants(self):

        url = urljoin(URLS['baseUrl'], '/plant/find_plant_list')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "sel_scope": 1,
            "sort_type": 1
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

    def get_powerplant(self, plantId):

        url = urljoin(URLS['baseUrl'], '/plant/get_plant_overview')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "plant_id": plantId
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

    def get_powerplant_devices(self, plantId):

        url = urljoin(URLS['baseUrl'], '/plant/get_plant_device_list')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "plant_id": plantId
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

    def get_powerplant_inverter(self, plantId, deviceId):

        url = urljoin(URLS['baseUrl'], '/device/doInverterDetail')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "plant_id": plantId,
            "deviceId": deviceId
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

    def get_powerplant_logger(self, plantId, loggerID):

        url = urljoin(URLS['baseUrl'], '/logger/get_logger_detail')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "plant_id": plantId,
            "gsn": loggerID
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

    def get_powerplant_condition(self, plantID):

        url = urljoin(URLS['baseUrl'], '/plant/get_plant_condition')
        headers = { "token": self.access_token }
        params = {

            "uid": self.user_id,
            "plant_id": plantID,
            "cityCode": "",
            "lan": "en"
        }
        r = requests.get(url, params=params, headers = headers )
        r.raise_for_status()
        return r.json()

def urljoin(*parts):
    """
    Join terms together with forward slashes
    Parameters
    ----------
    parts
    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url