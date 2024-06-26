"""
Collect playbyplayv3 endpoint data
"""
import datetime
from typing import Any, Dict

from swish_acquisition.constants import PLAY_BY_PLAY
from swish_acquisition.endpoints.base import Endpoint
from swish_acquisition.scheme.endpoints import PlayByPlayV3


class PlayByPlayV3Endpoint(Endpoint[PlayByPlayV3]):

    ENDPOINT: str = PLAY_BY_PLAY.endpoint_name

    def __init__(self, *args: Any, **kwargs: Any) -> None:
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
