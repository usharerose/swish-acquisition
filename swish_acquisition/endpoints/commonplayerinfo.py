"""
Collect commonplayerinfo endpoint data
"""
import datetime
from typing import Dict, Type

from swish_acquisition.endpoints.base import Endpoint
from swish_acquisition.scheme.endpoints import CommonPlayerInfo


class CommonPlayerInfoEndpoint(Endpoint):

    DATA_MODEL: Type[CommonPlayerInfo] = CommonPlayerInfo
    ENDPOINT: str = 'commonplayerinfo'

    def __init__(self, *args, **kwargs):
        super(CommonPlayerInfoEndpoint, self).__init__(*args, **kwargs)
        self.player_id: str = kwargs['player_id']
        self.game_date: datetime.date = kwargs['game_date']

    def get_params(self) -> Dict:
        return {
            'PlayerID': self.player_id
        }
