"""
Data Object of boxsummaryv3 endpoint response
"""
import datetime
from typing import List

from pydantic import BaseModel

from swish_acquisition.scheme.endpoints.meta import Meta


__all__ = ['BoxScoreSummaryV3', 'TeamGameOverallStats']


class GameArena(BaseModel):

    arenaId: int             # the identifier of the arena
    arenaName: str           # name of arena
    arenaCity: str           # located city of arena
    arenaState: str          # abbreviation of arena's located state
    arenaCountry: str        # abbreviation of arena's located country
    arenaTimezone: str
    arenaStreetAddress: str
    arenaPostalCode: str


class Official(BaseModel):

    personId: int    # the identifier of the official
    name: str        # full name of the official
    nameI: str       # shortcut of name
    firstName: str
    familyName: str
    jerseyNum: str   # jersey number of the official, need to be trimmed (raw like '55  ')
    assignment: str


class BroadCaster(BaseModel):

    broadcasterId: int
    broadcastDisplay: str           # short-cut display of broadcaster
    broadcasterDisplay: str         # full display of broadcaster
    broadcasterVideoLink: str = ''
    broadcasterTeamId: int = -1     # team's identifier for a local broadcaster, -1 for national broadcaster


class BroadCasters(BaseModel):

    nationalBroadcasters: List[BroadCaster]
    nationalRadioBroadcasters: List[BroadCaster]
    nationalOttBroadcasters: List[BroadCaster]
    homeTvBroadcasters: List[BroadCaster]
    homeRadioBroadcasters: List[BroadCaster]
    homeOttBroadcasters: List[BroadCaster]
    awayTvBroadcasters: List[BroadCaster]
    awayRadioBroadcasters: List[BroadCaster]
    awayOttBroadcasters: List[BroadCaster]


class TeamOverallStatsFieldStatistics(BaseModel):

    dummyKey: str = 'dummyValue'


class PeriodBasicScoreInfoItem(BaseModel):

    period: int      # period number, start from 1
    periodType: str  # Upper alphabets, such as 'REGULAR', 'OVERTIME'
    score: int       # score in this period


class PlayerBasicInfoItem(BaseModel):

    personId: int    # identifier of the player
    firstName: str
    familyName: str
    jerseyNum: str   # jersey number of the player, need to be trimmed (raw like '7   ')


class PlayerExtendedBasicInfoItem(PlayerBasicInfoItem):

    name: str        # full name of the player
    nameI: str       # shortcut of name


class TeamGameOverallStats(BaseModel):
    """
    Model of team's overall stats in a game
    """
    teamId: int                                  # identifier of a team
    teamName: str                                # name of a team, e.g. Lakers
    teamCity: str                                # location of a team, e.g. Los Angeles
    teamTricode: str                             # triple alphabet code of a team
    teamSlug: str                                # slug of a team
    teamWins: int                                # Winning games in a stage (regular season, play-in, each round of
    # playoff and finals)
    teamLosses: int                              # Lost games in a stage (regular season, play-in, each round of
    # playoff and finals)
    score: int                                   # score in a game
    inBonus: str = ''
    timeoutsRemaining: int = 0                   # remaining timeouts
    seed: int = 0                                # seed number among the conference, would be 0 for regular season
    # and play-in game
    statistics: TeamOverallStatsFieldStatistics  # TODO: investigate its meaning
    periods: List[PeriodBasicScoreInfoItem]
    players: List[PlayerExtendedBasicInfoItem]   # active players list
    inactives: List[PlayerBasicInfoItem]         # inactive players list


class TeamGameOverallStatsShortcut(BaseModel):
    """
    Model of team's overall stats in a game for historical meeting info
    """
    teamId: int       # identifier of a team
    teamCity: str     # location of a team, e.g. Los Angeles
    teamName: str     # name of a team, e.g. Lakers
    teamTricode: str  # triple alphabet code of a team
    teamSlug: str     # slug of a team
    score: int        # score in a game
    wins: int         # Winning games in a stage (regular season, play-in, each round of
    # playoff and finals)
    losses: int       # Lost games in a stage (regular season, play-in, each round of
    # playoff and finals)


class HistoricalMeetingBasicStats(BaseModel):

    recencyOrder: int               # order by game date
    gameId: str                     # the identifier of a game as numeric string
    gameTimeUTC: datetime.datetime  # game start time at UTC timezone with format %Y-%m-%dT%H:%M:%S.%fZ

    # game start time at US Eastern with format %Y-%m-%dT%H:%M:%S.%fZ
    # due to DST (Daylight Saving Time), it's difficult to set correct timezone info
    # advise using gameTimeUTC directly which is more universal
    gameEt: datetime.datetime

    gameStatus: int                 # the identifier of game status, such as 3 representing 'Final'
    gameStatusText: str             # semantic text of game status, such as 'Final'
    gameClock: str                  # format is PT%MM:%S.%fS
    awayTeam: TeamGameOverallStatsShortcut
    homeTeam: TeamGameOverallStatsShortcut


class LastFiveMeetingsObject(BaseModel):
    """
    Abstract statistics in last five meetings
    """
    meetings: List[HistoricalMeetingBasicStats]


class Statistics(BaseModel):
    """
    Field 'statistics' in each team item of 'pregameCharts'
    It illustrates the average stats per game of a team
    """
    points: float
    reboundsTotal: float
    assists: float
    steals: float
    blocks: float
    turnovers: float
    fieldGoalsPercentage: float
    threePointersPercentage: float
    freeThrowsPercentage: float
    pointsInThePaint: float
    pointsSecondChance: float
    pointsFastBreak: float
    playerPtsLeaderFirstName: str
    playerPtsLeaderFamilyName: str
    playerPtsLeaderId: int
    playerPtsLeaderPts: float
    playerRebLeaderFirstName: str
    playerRebLeaderFamilyName: str
    playerRebLeaderId: int
    playerRebLeaderReb: float
    playerAstLeaderFirstName: str
    playerAstLeaderFamilyName: str
    playerAstLeaderId: int
    playerAstLeaderAst: float
    playerBlkLeaderFirstName: str
    playerBlkLeaderFamilyName: str
    playerBlkLeaderId: int
    playerBlkLeaderBlk: float


class ExtendedStatistics(Statistics):
    """
    Field 'statistics' in each team item of 'postgameCharts'
    It illustrates the single game stats of a team
    """
    biggestLead: float
    leadChanges: float
    timesTied: float
    biggestScoringRun: float
    turnoversTeam: float
    turnoversTotal: float
    reboundsTeam: float
    pointsFromTurnovers: float
    benchPoints: float


class TeamSeasonOverallStats(BaseModel):
    """
    Model of team's overall stats in season's historical games
    """
    teamId: int                                  # identifier of a team
    teamCity: str                                # location of a team, e.g. Los Angeles
    teamName: str                                # name of a team, e.g. Lakers
    teamTricode: str                             # triple alphabet code of a team
    statistics: Statistics


class PreGameCharts(BaseModel):
    """
    Statistics of both teams before the game
    """
    homeTeam: TeamSeasonOverallStats
    awayTeam: TeamSeasonOverallStats


class TeamGameKeyStats(BaseModel):
    """
    Model of team's stats in the game
    """
    teamId: int                                  # identifier of a team
    teamCity: str                                # location of a team, e.g. Los Angeles
    teamName: str                                # name of a team, e.g. Lakers
    teamTricode: str                             # triple alphabet code of a team
    statistics: ExtendedStatistics


class PostGameCharts(BaseModel):
    """
    Statistics of both teams in the single game
    """
    homeTeam: TeamGameKeyStats
    awayTeam: TeamGameKeyStats


class BoxScoreSummary(BaseModel):
    """
    Model of 'boxScoreSummary' field for the raw data from boxscoresummaryv3 endpoint
    """
    gameId: str                     # the identifier of a game as numeric string
    gameCode: str                   # the semantic code of a game with format %Y%m%d/{awayTeamTricode}{homeTeamTricode}
    gameStatus: int                 # the identifier of game status, such as 3 representing 'Final'
    gameStatusText: str             # semantic text of game status, such as 'Final'
    period: int                     # realistic periods of a game, commonly 4, could be greater if it has OTs
    gameClock: str                  # format is PT%MM:%S.%fS
    gameTimeUTC: datetime.datetime  # game start time at UTC timezone with format %Y-%m-%dT%H:%M:%S.%fZ

    # game start time at US Eastern with format %Y-%m-%dT%H:%M:%S.%fZ
    # due to DST (Daylight Saving Time), it's difficult to set correct timezone info
    # advise using gameTimeUTC directly which is more universal
    gameEt: datetime.datetime

    awayTeamId: int                 # the identifier of away team
    homeTeamId: int                 # the identifier of home team
    duration: str                   # duration of a complete game with format %H%M
    attendance: int                 # the amount of attendance
    sellout: int                    # 1 standing for true, 0 for false
    seriesGameNumber: str           # when game is playoff or final game, with format 'Game %d'
    seriesText: str                 # when game is playoff or final game, such as '{teamTriCode} leads 1-0'
    ifNecessary: bool
    arena: GameArena
    officials: List[Official]
    broadcasters: BroadCasters
    homeTeam: TeamGameOverallStats
    awayTeam: TeamGameOverallStats
    lastFiveMeetings: LastFiveMeetingsObject
    pregameCharts: PreGameCharts
    postgameCharts: PostGameCharts
    videoAvailableFlag: int         # 1 standing for true, else false
    ptAvailable: int                # 1 standing for true, else false
    ptXYZAvailable: int             # 1 standing for true, else false
    whStatus: int                   # 1 standing for true, else false
    hustleStatus: int               # 1 standing for true, else false
    historicalStatus: int           # 1 standing for true, else false
    gameSubtype: str


class BoxScoreSummaryV3(BaseModel):
    """
    Model of raw data from boxscoresummaryv3 endpoint
    """
    meta: Meta
    boxScoreSummary: BoxScoreSummary
