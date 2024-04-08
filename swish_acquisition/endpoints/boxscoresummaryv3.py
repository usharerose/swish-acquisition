"""
Collect boxsummaryv3 endpoint data
"""
import datetime
from typing import Any, Dict, Optional

from swish_acquisition.constants import BOXSCORE_SUMMARY
from swish_acquisition.endpoints.base import Endpoint
from swish_acquisition.scheme.endpoints import BoxScoreSummaryV3
from swish_acquisition.scheme.endpoints.boxscoresummaryv3 import TeamGameOverallStats


class BoxScoreSummaryV3Endpoint(Endpoint[BoxScoreSummaryV3]):

    ENDPOINT: str = BOXSCORE_SUMMARY.endpoint_name

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(BoxScoreSummaryV3Endpoint, self).__init__(*args, **kwargs)
        self.game_id: str = kwargs['game_id']
        self.game_date: datetime.date = kwargs['game_date']

    def get_params(self) -> Dict:
        return {
            'GameID': self.game_id
        }

    def get_team_ids(self) -> Dict[str, Optional[int]]:
        away_team_id = home_team_id = None
        dm = self.get_data()
        if dm:
            away_team_id = dm.boxScoreSummary.awayTeamId
            home_team_id = dm.boxScoreSummary.homeTeamId
        return {
            'away': away_team_id,
            'home': home_team_id
        }

    def get_player_ids(self) -> Dict[str, Optional[list]]:
        away_player_ids = home_player_ids = None
        dm = self.get_data()
        if dm:
            away_player_ids = self._get_roster_ids_by_team(dm.boxScoreSummary.awayTeam)
            home_player_ids = self._get_roster_ids_by_team(dm.boxScoreSummary.homeTeam)
        return {
            'away': away_player_ids,
            'home': home_player_ids
        }

    @staticmethod
    def _get_roster_ids_by_team(team_game_stats: TeamGameOverallStats):
        player_ids = []
        for active_player in team_game_stats.players:
            player_ids.append(active_player.personId)
        for inactive_player in team_game_stats.inactives:
            player_ids.append(inactive_player.personId)

        player_ids.sort()
        return player_ids
