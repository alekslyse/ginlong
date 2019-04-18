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
        self.base_url = API_ENDPOINT
 
        
        self.username = None
        self.password = None
        self.user_id = None

        self.access_token = None



    async def authenticate(self, username, password):
        """Authenticate."""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                params = {'user_id': username, 'user_pass': password}
                response = await self._session.get(self.base_url, params=params)
            
            
            _LOGGER.info(
                "Response from Ginlong API: %s", response.status)
            self.data = await response.json()
            _LOGGER.debug(self.data)


        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from Ginlong API")
            raise exceptions.GinlongConnectionError



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


