"""
Collect and store Common Player Info raw data
"""
from typing import Any, Dict

from swish_acquisition.collectors.base import EndpointCollectorMixIn
from swish_acquisition.endpoints import CommonPlayerInfoEndpoint
from swish_acquisition.s3 import S3MixIn


class CommonPlayerInfoCollector(CommonPlayerInfoEndpoint, S3MixIn, EndpointCollectorMixIn):

    BUCKET_NAME = 'commonplayerinfo'
    OBJECT_NAME_PATTERN = '/{player_id}.json'

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # NOQA
        super().__init__(*args, **kwargs)

    def get_object_path_kwargs(self) -> Dict:
        return {
            'player_id': self.player_id
        }
