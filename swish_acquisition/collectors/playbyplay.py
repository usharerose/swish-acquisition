"""
Collect and store PlayByPlay raw data
"""
from typing import Dict

from swish_acquisition.collectors.base import EndpointCollectorMixIn
from swish_acquisition.endpoints import PlayByPlayV3Endpoint
from swish_acquisition.s3 import S3MixIn


class PlayByPlayCollector(PlayByPlayV3Endpoint, S3MixIn, EndpointCollectorMixIn):

    BUCKET_NAME = 'playbyplay'
    OBJECT_NAME_PATTERN = '/{year:04d}/{month:02d}/{day:02d}/{game_id}.json'

    def __init__(self, *args, **kwargs):  # NOQA
        super().__init__(*args, **kwargs)

    def get_object_path_kwargs(self) -> Dict:
        return {
            'year': self.game_date.year,
            'month': self.game_date.month,
            'day': self.game_date.day,
            'game_id': self.game_id
        }
