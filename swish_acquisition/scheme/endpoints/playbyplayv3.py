"""
Data Object of playbyplayv3 endpoint response
"""
from typing import List

from pydantic import BaseModel

from swish_acquisition.scheme.endpoints.meta import Meta


__all__ = ['PlayByPlayV3']


class PlayByPlayActionItem(BaseModel):
    """
    Model of specific action in a game
    """
    # the number of an event occurred in the game, which could be related to multiple actions
    # a steal and a bad pass, totally 2 actions, can be related to the same event
    actionNumber: int      # the number of an event occurred in the game, which could be related to multiple actions.
    # For example, a steal and a bad pass, totally 2 actions, can be related to the same event
    clock: str             # count down of a period, e.g. 'PT12M00.00S'
    period: int            # period number, start from 1
    teamId: int            # identifier of a team
    teamTricode: str       # triple alphabet code of team playing for
    personId: int          # the identifier of the player
    playerName: str        # player name
    playerNameI: str       # shortcut of player name
    xLegacy: int = 0       # x coordinates if action is a shot
    yLegacy: int = 0       # y coordinates if action is a shot
    shotDistance: int = 0  # distance to the rim if action is a shot which unit is feet
    shotResult: str = ''   # description of shot result if action is a shot
    isFieldGoal: int = 0   # 1 if shot is a field goal, else (including non-shot action) 0
    scoreHome: str = ''    # accumulative score of home team, only show the value when action is about shot made
    scoreAway: str = ''    # accumulative score of away team, only show the value when action is about shot made
    pointsTotal: int = 0   # total score of the game with both teams, only show the value
    # when action is about shot made
    location: str
    description: str       # natural language description of the action
    actionType: str
    subType: str
    videoAvailable: int    # 1 if there was a video recording this action, else 0
    actionId: int          # identifier of the action


class PlayByPlayGame(BaseModel):
    """
    Model of game's Play-by-Play data
    """
    gameId: str          # the identifier of a game as numeric string
    videoAvailable: int  # 1 is positive which is available, else 0
    actions: List[PlayByPlayActionItem]


class PlayByPlayV3(BaseModel):
    """
    Model of raw data from playbyplayv3 endpoint
    """
    meta: Meta
    game: PlayByPlayGame
