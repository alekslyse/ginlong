import asyncio
import logging
import socket

import aiohttp
import async_timeout

from . import exceptions

DEFAULT_TIMEOUT = 10
API_ENDPOINT = 'http://apic-cdn.solarman.cn/v/ap.2.0'

_LOGGER = logging.getLogger(__name__)


class Ginlong(object):

    def __init__(self, loop, session):

        self._loop = loop
        self._session = session
        self.data = {}
        self.plants = {}
        self.base_url = API_ENDPOINT
 
        
        self.username = None
        self.password = None
        self.user_id = None

        self.access_token = None
        self.plant_id = None



    async def authenticate(self, username, password):
        """Authenticate."""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                params = {'user_id': username, 'user_pass': password}
                response = await self._session.get(self.base_url+'/cust/user/login', params=params)
            
            
                _LOGGER.info(
                    "Response from Ginlong API: %s", response.status)
                auth = await response.json(content_type=None)
                _LOGGER.debug(self.data)

                if int(auth['result']) == 5:
                    raise exceptions.InvalidLogin("Wrong password")

                elif int(auth['result']) == 11:
                    raise exceptions.InvalidLogin("Wrong username")

                elif int(auth['result']) == 11:
                    raise exceptions.InvalidLogin("Wrong username")
                
                elif 'token' not in auth:
                    raise exceptions.InvalidLogin("Unknown Error")

                self.access_token = auth['token']

                return True


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError


    async def get_plants(self):
        """Get all power plants."""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                params = {'uid': self.user_id, 'sel_scope': 1, 'sort_type': 1}
                headers = {'token': self.access_token}
                response = await self._session.get(self.base_url+'/plant/find_plant_list', params=params, headers=headers)
            
            
                


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError


    @property
    def token(self):
        """Return the token."""
        return self.access_token

    @property
    def uid(self):
        """Return the user id."""
        return self.user_id

    @property
    def plant(self):
        """Return the plant id."""
        return self.plant_id