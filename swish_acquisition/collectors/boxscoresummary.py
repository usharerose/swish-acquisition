"""
Collect and store Boxscore Summary raw data
"""
from typing import Any, Dict

from swish_acquisition.collectors.base import EndpointCollectorMixIn
from swish_acquisition.endpoints import BoxScoreSummaryV3Endpoint
from swish_acquisition.s3 import S3MixIn


class BoxscoreSummaryCollector(BoxScoreSummaryV3Endpoint, S3MixIn, EndpointCollectorMixIn):

    BUCKET_NAME = 'boxscoresummary'
    OBJECT_NAME_PATTERN = '/{year:04d}/{month:02d}/{day:02d}/{game_id}.json'

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # NOQA
        super().__init__(*args, **kwargs)

    def get_object_path_kwargs(self) -> Dict:
        return {
            'year': self.game_date.year,
            'month': self.game_date.month,
            'day': self.game_date.day,
            'game_id': self.game_id
        }
