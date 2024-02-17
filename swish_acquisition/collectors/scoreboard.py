"""
Collect and store scoreboard raw data
"""
from typing import Dict

from swish_acquisition.collectors.base import EndpointCollectorMixIn
from swish_acquisition.endpoints import ScoreboardV3Endpoint
from swish_acquisition.s3 import S3MixIn


class ScoreboardCollector(ScoreboardV3Endpoint, S3MixIn, EndpointCollectorMixIn):

    BUCKET_NAME = 'scoreboard'
    OBJECT_NAME_PATTERN = '/{year:04d}/{month:02d}/{day:02d}.json'

    def __init__(self, *args, **kwargs):  # NOQA
        super().__init__(*args, **kwargs)

    def get_object_path_kwargs(self) -> Dict:
        return {
            'year': self.game_date.year,
            'month': self.game_date.month,
            'day': self.game_date.day
        }
