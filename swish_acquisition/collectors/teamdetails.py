"""
Collect and store Team Details raw data
"""
from typing import Any, Dict

from swish_acquisition.collectors.base import EndpointCollectorMixIn
from swish_acquisition.endpoints import TeamDetailsEndpoint
from swish_acquisition.s3 import S3MixIn


class TeamDetailsCollector(TeamDetailsEndpoint, S3MixIn, EndpointCollectorMixIn):

    BUCKET_NAME = 'teamdetails'
    OBJECT_NAME_PATTERN = '/{team_id}.json'

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # NOQA
        super().__init__(*args, **kwargs)

    def get_object_path_kwargs(self) -> Dict:
        return {
            'team_id': self.team_id
        }
