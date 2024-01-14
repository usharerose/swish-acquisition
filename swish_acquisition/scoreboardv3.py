"""
Collect scoreboardv3 endpoint data
"""
import datetime
from typing import Dict, Type

from swish_acquisition.base import (
    DATE_FORMAT_V3,
    Endpoint
)
from swish_acquisition.scheme import ScoreboardV3


class ScoreboardV3Endpoint(Endpoint):

    DATA_MODEL: Type[ScoreboardV3] = ScoreboardV3
    ENDPOINT: str = 'scoreboardv3'

    def __init__(self, *args, **kwargs):
        super(ScoreboardV3Endpoint, self).__init__(*args, **kwargs)
        self.game_date: datetime.date = kwargs['game_date']
        self.league_id: str = kwargs['league_id']

    def get_params(self) -> Dict:
        return {
            'GameDate': self.game_date.strftime(DATE_FORMAT_V3),
            'LeagueID': self.league_id
        }
