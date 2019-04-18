    
"""Exceptions for Ginlong API client."""


class GinlongError(Exception):
    """General Ginlong exception occurred."""

    pass


class InvalidLogin(Exception):
    """Invalid login exception."""

    pass

class GinlongConnectionError(Exception):

    pass