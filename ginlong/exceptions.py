    
"""Exceptions for Ginlong API client."""


class Ginlong(Exception):
    """General Ginlong exception occurred."""

    pass


class InvalidLogin(Exception):
    """Invalid login exception."""

    pass

class GinlongConnectionError(Exception):

    pass