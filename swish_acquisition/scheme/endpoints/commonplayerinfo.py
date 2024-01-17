"""
Data Object of commonplayerinfo endpoint response
"""
import datetime
from typing import List, NamedTuple, Optional, Union

from pydantic import BaseModel


__all__ = ['CommonPlayerInfo']


class PlayerIDParameter(BaseModel):

    PlayerID: int


class LeagueIDParameter(BaseModel):

    LeagueID: Optional[str] = None


class CommonPlayerInfoRowSetItem(NamedTuple):
    """
    Model of CommonPlayerInfo's 'rowSet' field's item
    Raw data is a list originally
    """
    PERSON_ID: int                         # identifier of player
    FIRST_NAME: str                        # first name of player
    LAST_NAME: str                         # last name of player
    DISPLAY_FIRST_LAST: str                # Display name, connect FIRST_NAME and LAST_NAME with space
    DISPLAY_LAST_COMMA_FIRST: str          # Display name, connect LAST_NAME and FIRST_NAME with comma
    DISPLAY_FI_LAST: str                   # Display name, connect initial first name and last name with space
    PLAYER_SLUG: str                       # slug of player
    BIRTHDATE: datetime.datetime           # datetime of birthday
    SCHOOL: str                            # school attended before drafted,
    # could be region or club name who didn't study in US
    COUNTRY: str                           # home country of player
    LAST_AFFILIATION: str                  # concat SCHOOL and COUNTRY with forward slash
    HEIGHT: str                            # concat ft and in of player height with dashed line
    WEIGHT: str                            # weight of player, unit is Lb
    SEASON_EXP: int                        # count of experienced seasons
    JERSEY: str                            # jersey number of player
    POSITION: str                          # position of player
    ROSTERSTATUS: str                      # represent the player is still in the league (Active) or not (Inactive)
    GAMES_PLAYED_CURRENT_SEASON_FLAG: str  # represent the player plays in this season (Y) or not (N)
    TEAM_ID: int                           # identifier of team, most representative,
    # or the latest one for retired player
    TEAM_NAME: str                         # name of team
    TEAM_ABBREVIATION: str                 # tri-code as team name abbreviation
    TEAM_CODE: str                         # code of team
    TEAM_CITY: str                         # city of team location
    PLAYERCODE: str                        # code of player
    FROM_YEAR: int                         # season year (less one) when player started play in the league
    TO_YEAR: int                           # latest season year (less one) when player play in the league
    DLEAGUE_FLAG: str                      # Y or N
    NBA_FLAG: str                          # Y or N
    GAMES_PLAYED_FLAG: str                 # Y or N
    DRAFT_YEAR: str                        # year drafted or 'Undrafted'
    DRAFT_ROUND: str                       # round or 'Undrafted'
    DRAFT_NUMBER: str                      # total number or 'Undrafted'
    GREATEST_75_FLAG: str                  # Y or N


class CommonPlayerInfoResultSet(BaseModel):

    name: str = 'CommonPlayerInfo'
    headers: List[str] = [
        'PERSON_ID',
        'FIRST_NAME',
        'LAST_NAME',
        'DISPLAY_FIRST_LAST',
        'DISPLAY_LAST_COMMA_FIRST',
        'DISPLAY_FI_LAST',
        'PLAYER_SLUG',
        'BIRTHDATE',
        'SCHOOL',
        'COUNTRY',
        'LAST_AFFILIATION',
        'HEIGHT',
        'WEIGHT',
        'SEASON_EXP',
        'JERSEY',
        'POSITION',
        'ROSTERSTATUS',
        'GAMES_PLAYED_CURRENT_SEASON_FLAG',
        'TEAM_ID',
        'TEAM_NAME',
        'TEAM_ABBREVIATION',
        'TEAM_CODE',
        'TEAM_CITY',
        'PLAYERCODE',
        'FROM_YEAR',
        'TO_YEAR',
        'DLEAGUE_FLAG',
        'NBA_FLAG',
        'GAMES_PLAYED_FLAG',
        'DRAFT_YEAR',
        'DRAFT_ROUND',
        'DRAFT_NUMBER',
        'GREATEST_75_FLAG'
    ]
    rowSet: List[CommonPlayerInfoRowSetItem]


class PlayerHeadlineStatsRowSetItem(NamedTuple):
    """
    Model of PlayerHeadlineStats's 'rowSet' field's item
    Raw data is a list originally
    """
    PLAYER_ID: int             # identifier of player
    PLAYER_NAME: str           # name of player
    TimeFrame: str             # default is ‘career’
    PTS: float                 # career average points
    AST: float                 # career average assists
    REB: float                 # career average rebounds
    ALL_STAR_APPEARANCES: int  # count of all star appearances


class PlayerHeadlineStatsResultSet(BaseModel):

    name: str = 'PlayerHeadlineStats'
    headers: List[str] = [
        'PLAYER_ID',
        'PLAYER_NAME',
        'TimeFrame',
        'PTS',
        'AST',
        'REB',
        'ALL_STAR_APPEARANCES'
    ]
    rowSet: List[PlayerHeadlineStatsRowSetItem]


class AvailableSeasonsRowSetItem(NamedTuple):
    """
    Model of AvailableSeasons's 'rowSet' field's item
    Raw data is a list originally
    """
    SEASON_ID: str  # identifier of season. pattern is ^(?P<season_stage_id>\d{1})(?P<season_id>\d{4})$


class AvailableSeasonsResultSet(BaseModel):

    name: str = 'AvailableSeasons'
    headers: List[str] = [
        'SEASON_ID'
    ]
    rowSet: List[AvailableSeasonsRowSetItem]


class CommonPlayerInfo(BaseModel):
    """
    Model of raw data from commonplayerinfo endpoint
    """
    resource: str = 'commonplayerinfo'
    parameters: List[Union[PlayerIDParameter, LeagueIDParameter]]
    resultSets: List[
        Union[
            CommonPlayerInfoResultSet,
            PlayerHeadlineStatsResultSet,
            AvailableSeasonsResultSet
        ]
    ]
