"""
Collect boxsummaryv3 endpoint data
"""
import datetime
from typing import Dict, Type

from swish_acquisition.endpoints.base import Endpoint
from swish_acquisition.scheme.endpoints import BoxScoreSummaryV3


class BoxScoreSummaryV3Endpoint(Endpoint):

    DATA_MODEL: Type[BoxScoreSummaryV3] = BoxScoreSummaryV3
    ENDPOINT: str = 'boxscoresummaryv3'

    def __init__(self, *args, **kwargs):
        super(BoxScoreSummaryV3Endpoint, self).__init__(*args, **kwargs)
        self.game_id: str = kwargs['game_id']
        self.game_date: datetime.date = kwargs['game_date']

    def get_params(self) -> Dict:
        return {
            'GameID': self.game_id
        }
