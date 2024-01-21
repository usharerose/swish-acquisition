"""
Data Object of teamdetails endpoint response
"""
from typing import List, NamedTuple, Optional, Union

from pydantic import BaseModel


__all__ = ['TeamDetails']


class CommonPlayerInfoParameters(BaseModel):

    TeamID: int  # identifier of team


class TeamBackgroundRowSetItem(NamedTuple):
    """
    Model of TeamBackground's 'rowSet' field's item
    Raw data is a list originally

    since CITY is the real location so that can't combine with NICKNAME for team full name,
    need to use boxScoreSummary.[away|home]Team.teamCity as team's first name
    """
    TEAM_ID: int                  # identifier of team
    ABBREVIATION: str             # tri-code of team
    NICKNAME: str                 # name of team
    YEARFOUNDED: int              # year when team was founded
    CITY: str                     # city or region of team
    ARENA: str                    # arena of team
    ARENACAPACITY: Optional[str]  # capacity of arena
    OWNER: str                    # name of team owner, boss or parent team
    GENERALMANAGER: str           # name of general manager, could be ' ' or '' if no info
    HEADCOACH: str                # name of head coach
    DLEAGUEAFFILIATION: str       # name of Development League team, also could be 'No Affiliate' when no D-League team,
    # or upper tri-code of parent team for D-League team


class TeamBackgroundResultSet(BaseModel):

    name: str = 'TeamBackground'
    headers: List[str] = [
        'TEAM_ID',
        'ABBREVIATION',
        'NICKNAME',
        'YEARFOUNDED',
        'CITY',
        'ARENA',
        'ARENACAPACITY',
        'OWNER',
        'GENERALMANAGER',
        'HEADCOACH',
        'DLEAGUEAFFILIATION'
    ]
    rowSet: List[TeamBackgroundRowSetItem]


class TeamHistoryRowSetItem(NamedTuple):
    """
    Model of TeamHistory's 'rowSet' field's item
    Raw data is a list originally
    """
    TEAM_ID: int         # identifier of team
    CITY: str            # city or region of team
    NICKNAME: str        # name of team
    YEARFOUNDED: int     # season year that started
    YEARACTIVETILL: int  # season year that ended


class TeamHistoryResultSet(BaseModel):

    name: str = 'TeamHistory'
    headers: List[str] = [
        'TEAM_ID',
        'CITY',
        'NICKNAME',
        'YEARFOUNDED',
        'YEARACTIVETILL'
    ]
    rowSet: List[TeamHistoryRowSetItem]


class TeamSocialSitesRowSetItem(NamedTuple):
    """
    Model of TeamSocialSites' 'rowSet' field's item
    Raw data is a list originally
    """
    ACCOUNTTYPE: str   # type of social media
    WEBSITE_LINK: str  # link of social media


class TeamSocialSitesResultSet(BaseModel):

    name: str = 'TeamSocialSites'
    headers: List[str] = [
        'ACCOUNTTYPE',
        'WEBSITE_LINK'
    ]
    rowSet: List[TeamSocialSitesRowSetItem]


class TeamAwardsRowSetItem(NamedTuple):
    """
    Model of TeamAwards' 'rowSet' field's item
    Raw data is a list originally
    """
    YEARAWARDED: int   # natural year (not season year) when win the award
    OPPOSITETEAM: Optional[str]  # team full name


class TeamAwardsChampionshipsResultSet(BaseModel):

    name: str = 'TeamAwardsChampionships'
    headers: List[str] = [
        'YEARAWARDED',
        'OPPOSITETEAM'
    ]
    rowSet: List[TeamAwardsRowSetItem]


class TeamAwardsConfResultSet(BaseModel):

    name: str = 'TeamAwardsConf'
    headers: List[str] = [
        'YEARAWARDED',
        'OPPOSITETEAM'
    ]
    rowSet: List[TeamAwardsRowSetItem]


class TeamAwardsDivResultSet(BaseModel):

    name: str = 'TeamAwardsDiv'
    headers: List[str] = [
        'YEARAWARDED',
        'OPPOSITETEAM'
    ]
    rowSet: List[TeamAwardsRowSetItem]


class TeamRemarkablePersonRowSetItem(NamedTuple):
    """
    Model of TeamHof's 'rowSet' field's item
    Raw data is a list originally
    """
    PLAYERID: Optional[int]  # identifier of player
    PLAYER: str              # full name of player
    POSITION: str            # shortcut of position
    JERSEY: Optional[str]    # jersey number, but null from response
    SEASONSWITHTEAM: str     # various pattern, e.g. '1984', '1984-1985', '1985-1993, 1995-1998'.
    # and start and end standards are not consistent
    YEAR: int                # natural year when induction


class TeamHofResultSet(BaseModel):

    name: str = 'TeamHof'
    headers: List[str] = [
        'PLAYERID',
        'PLAYER',
        'POSITION',
        'JERSEY',
        'SEASONSWITHTEAM',
        'YEAR'
    ]
    rowSet: List[TeamRemarkablePersonRowSetItem]


class TeamRetiredResultSet(BaseModel):

    name: str = 'TeamRetired'
    headers: List[str] = [
        'PLAYERID',
        'PLAYER',
        'POSITION',
        'JERSEY',
        'SEASONSWITHTEAM',
        'YEAR'
    ]
    rowSet: List[TeamRemarkablePersonRowSetItem]


class TeamDetails(BaseModel):
    """
    Model of raw data from teamdetails endpoint
    """
    resource: str = 'teamdetails'
    parameters: CommonPlayerInfoParameters
    resultSets: List[
        Union[
            TeamBackgroundResultSet,
            TeamHistoryResultSet,
            TeamSocialSitesResultSet,
            TeamAwardsConfResultSet,
            TeamAwardsDivResultSet,
            TeamHofResultSet,
            TeamRetiredResultSet
        ]
    ]
