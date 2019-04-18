import asyncio
import logging
import socket

import aiohttp
import async_timeout

from . import exceptions

DEFAULT_TIMEOUT = 10
API_ENDPOINT = 'http://apic-cdn.solarman.cn/v/ap.2.0'

_LOGGER = logging.getLogger(__name__)


class Ginlong():

    def __init__(self, loop, session):

        self._loop = loop
        self._session = session
        self.data = {}
        self.plants = {}
        self.plant = []
        self.plant_ids = []
        self.base_url = API_ENDPOINT
        self.first_update_done = False
 
        
        self.username = None
        self.password = None
        self.user_id = None

        self.access_token = None
        self.plant_id = None
        self._test = 123



    async def authenticate(self, username, password):
        """Authenticate."""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                params = {'user_id': username, 'user_pass': password}
                response = await self._session.get(self.base_url+'/cust/user/login', params=params)
            
            
                _LOGGER.info(
                    "Response from Ginlong API: %s", response.status)
                auth = await response.json(content_type=None)
                _LOGGER.debug(auth)

                if int(auth['result']) == 5:
                    raise exceptions.InvalidLogin("Wrong password")

                elif int(auth['result']) == 11:
                    raise exceptions.InvalidLogin("Wrong username")

                elif int(auth['result']) == 11:
                    raise exceptions.InvalidLogin("Wrong username")
                
                elif 'token' not in auth:
                    raise exceptions.InvalidLogin("Unknown Error")

                self.access_token = auth['token']
                self.user_id = auth['uid']

                return True


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError

        

    async def update_info(self):
        try:
            async with async_timeout.timeout(5, loop=self._loop):

                headers = {'token': self.access_token}
                params = {
                    "uid": self.user_id,
                    "sel_scope": 1,
                    "sort_type": 1
                }
                response = await self._session.get(self.base_url+'/plant/find_plant_list', params=params, headers=headers)
            
                _LOGGER.info(
                    "Response from Ginlong API: %s", response.status)
                plants = await response.json(content_type=None)
                _LOGGER.debug(self.plants)

                

                for plant in plants['list']:
                    self.plant_ids.append(plant['plant_id'])


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError

        

        self.first_update_done = True
        

    async def get_plant(self, plant_id):
        """Return one plant."""
        if plant_id not in self.plant_ids:
            _LOGGER.error("Could not find any Plants with id: %s", plant_id)
            return None

        if plant_id not in self.plants.keys():
            self.plants[plant_id] = GinlongPlant(plant_id, self)

        return self.plants[plant_id]

    

    @property
    def get_plants(self):
        """Return all plants."""
        return self.plant_ids
    

class GinlongPlant():

    def __init__(self, plant_id, parent):
        """Initialize the Ginlong plnat class."""
        self.plant_id = plant_id
        self.name = None
        self.current_production = None
        self.token = parent._test
        self._parent = parent
        self.power_accumilitated = None
        self.power_day = None
        self.power = None
        
    async def update_info(self):
        """Authenticate."""
        try:
            async with async_timeout.timeout(5, loop=self._parent._loop):

                headers = { "token": self._parent.access_token }

                params = {
                    "uid": self._parent.user_id,
                    "plant_id": self.plant_id
                }
                response = await self._parent._session.get(self._parent.base_url+'/plant/get_plant_overview', params=params, headers=headers)

                _LOGGER.info(
                    "Response from Ginlong API: %s", response.status)
                plant = await response.json(content_type=None)

                power_out = plant['power_out']
                self.power_accumilitated = power_out['energy_accu']
                self.power_day = power_out['energy_day']
                self.power = power_out['power']


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError

    @property
    def get_name(self):
        """Return all plants."""
        return "Disney"
    @property
    def get_power(self):
        """Return all plants."""
        return self.power

    @property
    def get_accumulated(self):
        """Return all plants."""
        return self.power_accumilitated

    @property
    def get_total_power_day(self):
        """Return all plants."""
        return self.power_day


    @property
    def get_test(self):
        """Return all plants."""
        return self.token