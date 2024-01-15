"""
Data Object of Meta in NBA Stats endpoint response data
"""
import datetime

from pydantic import BaseModel


__all__ = ['Meta']


class Meta(BaseModel):
    """
    Meta of the request to stats.nba.com
    """
    version: int = 1
    request: str
    time: datetime.datetime  # format is %Y-%m-%dT%H:%M:%S.%fZ
