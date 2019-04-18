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
        


    @property
    def get_plants(self):
        """Return all plants."""

        return self.plants['list']

    @property
    def get_plant(self, plantId):
        """Return one plant."""
        if plantId not in self.plant_ids:
            _LOGGER.error("Could not find any Plants with id: %s", plantId)
            return None

        if plantId not in self.plants.keys():
            self.plants[plantId] = GinlongPlant(plantId, self)

        return self.plants[plantId]

class GinlongPlant():

    def __init__(self, plant_id, parent):
        """Initialize the Ginlong plnat class."""
        self.plant_id = plant_id
        self.name = None
        self.current_production = None
        self.token = parent._test


    @property
    async def name(self):
        """Return all plants."""
        return "Disney"

    @property
    async def test(self):
        """Return all plants."""
        return self.token