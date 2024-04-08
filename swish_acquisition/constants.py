"""
Constants
"""
from dataclasses import dataclass


@dataclass
class StatSourceMeta:

    source_name: str
    bucket_name: str
    endpoint_name: str


BOXSCORE_SUMMARY = StatSourceMeta(
    source_name='boxscore_summary',
    bucket_name='boxscoresummary',
    endpoint_name='boxscoresummaryv3'
)
COMMON_PLAYER_INFO = StatSourceMeta(
    source_name='common_player_info',
    bucket_name='commonplayerinfo',
    endpoint_name='commonplayerinfo'
)
PLAY_BY_PLAY = StatSourceMeta(
    source_name='play_by_play',
    bucket_name='playbyplay',
    endpoint_name='playbyplayv3'
)
SCOREBOARD = StatSourceMeta(
    source_name='scoreboard',
    bucket_name='scoreboard',
    endpoint_name='scoreboardv3'
)
TEAM_DETAILS = StatSourceMeta(
    source_name='team_details',
    bucket_name='teamdetails',
    endpoint_name='teamdetails'
)


REGISTERED_STAT_SOURCES = [
    BOXSCORE_SUMMARY,
    COMMON_PLAYER_INFO,
    PLAY_BY_PLAY,
    SCOREBOARD,
    TEAM_DETAILS
]
