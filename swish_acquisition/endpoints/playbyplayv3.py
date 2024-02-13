"""
Collect playbyplayv3 endpoint data
"""
import datetime
from typing import Dict, Type

from swish_acquisition.base import (
    Endpoint
)
from swish_acquisition.scheme.endpoints import PlayByPlayV3


class PlayByPlayV3Endpoint(Endpoint):

    DATA_MODEL: Type[PlayByPlayV3] = PlayByPlayV3
    ENDPOINT: str = 'playbyplayv3'

    def __init__(self, *args, **kwargs):
        super(PlayByPlayV3Endpoint, self).__init__(*args, **kwargs)
        self.game_id: str = kwargs['game_id']
        self.game_date: datetime.date = kwargs['game_date']
        self.start_period: int = kwargs.get('start_period', 0)
        self.end_period: int = kwargs.get('end_period', 0)

    def get_params(self) -> Dict:
        return {
            'GameID': self.game_id,
            'StartPeriod': self.start_period,
            'EndPeriod': self.end_period
        }
