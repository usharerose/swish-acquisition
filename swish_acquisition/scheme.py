"""
Data Object of scoreboardv3 endpoint response
"""
import datetime
from typing import List

from pydantic import BaseModel


__all__ = ['ScoreboardV3']


class GameLeaderItem(BaseModel):
    """
    Model of game leader
    """
    personId: int     # the identifier of the player
    name: str         # player name
    playerSlug: str   # slug of player
    jerseyNum: str    # jersey number
    position: str     # position on the court
    teamTricode: str  # triple alphabet code of team playing for
    points: int
    rebounds: int
    assists: int


class GameLeaders(BaseModel):
    """
    Model of single game stats leaders
    """
    homeLeaders: GameLeaderItem
    awayLeaders: GameLeaderItem


class TeamLeaderItem(BaseModel):
    """
    Model of team leader
    """
    personId: int     # the identifier of the player
    name: str         # player name
    playerSlug: str   # slug of player
    jerseyNum: str    # jersey number
    position: str     # position on the court
    teamTricode: str  # triple alphabet code of team playing for
    points: float
    rebounds: float
    assists: float


class TeamLeaders(BaseModel):
    """
    Model of teams' stats leaders
    """
    homeLeaders: TeamLeaderItem
    awayLeaders: TeamLeaderItem
    seasonLeadersFlag: int


class BroadCaster(BaseModel):
    """
    Model of game broadcaster
    """
    broadcasterId: int
    broadcastDisplay: str


class BroadCasters(BaseModel):
    """
    Model of game broadcasters
    """
    nationalBroadcasters: List[BroadCaster]
    nationalRadioBroadcasters: List[BroadCaster]
    nationalOttBroadcasters: List[BroadCaster]
    homeTvBroadcasters: List[BroadCaster]
    homeRadioBroadcasters: List[BroadCaster]
    homeOttBroadcasters: List[BroadCaster]
    awayTvBroadcasters: List[BroadCaster]
    awayRadioBroadcasters: List[BroadCaster]
    awayOttBroadcasters: List[BroadCaster]


class ScoreboardPeriodItem(BaseModel):
    """
    Model of single period for scoreboard
    """
    period: int      # period number, start from 1
    periodType: str  # Upper alphabets, such as 'REGULAR', 'OVERTIME'
    score: int       # score in this period


class TeamGameOverall(BaseModel):
    """
    Model of team's overall stats in a game
    """
    teamId: int                          # identifier of a team
    teamName: str                        # name of a team, e.g. Lakers
    teamCity: str                        # location of a team, e.g. Los Angeles
    teamTricode: str                     # triple alphabet code of a team
    teamSlug: str                        # slug of a team
    wins: int                            # Winning games in a stage
    # (regular season, play-in, each round of playoff and finals)
    losses: int                          # Lost games in a stage
    # (regular season, play-in, each round of playoff and finals)
    seed: int                            # seed number among the conference,
    # would be 0 for regular season and play-in game
    score: int                           # score in a game
    inBonus: None
    timeoutsRemaining: int
    periods: List[ScoreboardPeriodItem]


class Game(BaseModel):
    """
    Model of single game data
    """
    gameId: str                     # the identifier of a game as numeric string
    gameCode: str                   # the semantic code of a game with format %Y%m%d/{awayTeamTricode}{homeTeamTricode}
    gameStatus: int                 # the identifier of game status, such as 3 representing 'Final'
    gameStatusText: str             # semantic text of game status, such as 'Final'
    period: int                     # realistic periods of a game, commonly 4, could be greater if it has OTs
    regulationPeriods: int          # commonly 4
    gameClock: str
    gameTimeUTC: datetime.datetime  # game start time at UTC timezone
    gameEt: datetime.datetime       # game start time at US Eastern. due to DST (Daylight Saving Time),
    # it's difficult to set correct timezone info. advise using gameTimeUTC directly which is more universal
    seriesGameNumber: str           # when game is playoff or final game, with format 'Game %d'
    seriesText: str                 # when game is playoff or final game, such as '{teamTriCode} leads 1-0'
    seriesConference: str           # when game is playoff or final game, such as 'East', 'West', or 'NBA Finals'
    poRoundDesc: str                # Playoff round description, only for Playoff game, such as 'Conf. Finals'
    ifNecessary: bool
    gameSubtype: str
    gameLeaders: GameLeaders
    teamLeaders: TeamLeaders
    broadcasters: BroadCasters
    homeTeam: TeamGameOverall
    awayTeam: TeamGameOverall


class DailyScoreboard(BaseModel):
    """
    Model of scoreboard data
    """
    gameDate: datetime.date  # the date of the game, which is a string with format %Y-%m-%d
    leagueId: str            # the identifier of league, such as '00' as National Basketball Association
    leagueName: str = ''     # the name of league
    games: List[Game]


class Meta(BaseModel):
    """
    Meta of the request to stats.nba.com
    """
    version: int = 1
    request: str
    time: datetime.datetime  # format is %Y-%m-%dT%H:%M:%S.%fZ


class ScoreboardV3(BaseModel):
    """
    Model of raw data from scoreboardv3 endpoint
    """
    meta: Meta
    scoreboard: DailyScoreboard
