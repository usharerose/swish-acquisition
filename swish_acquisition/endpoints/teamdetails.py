"""
Collect teamdetails endpoint data
"""
import datetime
from typing import Any, Dict

from swish_acquisition.endpoints.base import Endpoint
from swish_acquisition.scheme.endpoints import TeamDetails


class TeamDetailsEndpoint(Endpoint[TeamDetails]):

    ENDPOINT: str = 'teamdetails'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TeamDetailsEndpoint, self).__init__(*args, **kwargs)
        self.team_id: int = kwargs['team_id']
        self.game_date: datetime.date = kwargs['game_date']

    def get_params(self) -> Dict:
        return {
            'TeamID': self.team_id
        }
