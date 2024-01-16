"""
Unittest cases for playbyplayv3 endpoints data scheme
"""
import json
from unittest import TestCase

from swish_acquisition.scheme.endpoints import PlayByPlayV3


with open('tests/data/endpoints/playbyplayv3/0040900407.json', 'r') as fp:
    PLAYBYPLAY_V3_DATA = json.load(fp)


class PlayByPlayV3EndpointSchemeTestCases(TestCase):

    def setUp(self):
        self.data_scheme = PlayByPlayV3.model_validate(PLAYBYPLAY_V3_DATA)

    def test_playbyplay_basic_info(self):
        game = self.data_scheme.game
        self.assertEqual(game.gameId, '0040900407')
        self.assertIsInstance(game.actions, list)

    def test_playbyplay_action(self):
        sample_action, *_ = self.data_scheme.game.actions
        self.assertEqual(sample_action.actionNumber, 0)
        self.assertEqual(sample_action.clock, 'PT12M00.00S')
        self.assertEqual(sample_action.period, 1)
        self.assertEqual(sample_action.teamId, 0)
        self.assertEqual(sample_action.teamTricode, '')
        self.assertEqual(sample_action.personId, 0)
        self.assertEqual(sample_action.playerName, '')
        self.assertEqual(sample_action.playerNameI, '')
        self.assertEqual(sample_action.xLegacy, 0)
        self.assertEqual(sample_action.yLegacy, 0)
        self.assertEqual(sample_action.shotDistance, 0)
        self.assertEqual(sample_action.shotResult, '')
        self.assertEqual(sample_action.isFieldGoal, 0)
        self.assertEqual(sample_action.scoreHome, '0')
        self.assertEqual(sample_action.scoreAway, '0')
        self.assertEqual(sample_action.pointsTotal, 0)
        self.assertEqual(sample_action.location, '')
        self.assertEqual(sample_action.description, 'Start of 1st Period (9:08 PM EST)')
        self.assertEqual(sample_action.actionType, 'period')
        self.assertEqual(sample_action.subType, 'start')
        self.assertEqual(sample_action.videoAvailable, 0)
        self.assertEqual(sample_action.actionId, 1)

    def test_playbyplay_action_with_team(self):
        sample_action = self.data_scheme.game.actions[1]
        self.assertEqual(sample_action.actionNumber, 1)
        self.assertEqual(sample_action.clock, 'PT12M00.00S')
        self.assertEqual(sample_action.period, 1)
        self.assertEqual(sample_action.teamId, 1610612747)
        self.assertEqual(sample_action.teamTricode, 'LAL')
        self.assertEqual(sample_action.personId, 101115)
        self.assertEqual(sample_action.playerName, 'Bynum')
        self.assertEqual(sample_action.playerNameI, 'A. Bynum')
        self.assertEqual(sample_action.xLegacy, 0)
        self.assertEqual(sample_action.yLegacy, 0)
        self.assertEqual(sample_action.shotDistance, 0)
        self.assertEqual(sample_action.shotResult, '')
        self.assertEqual(sample_action.isFieldGoal, 0)
        self.assertEqual(sample_action.scoreHome, '')
        self.assertEqual(sample_action.scoreAway, '')
        self.assertEqual(sample_action.pointsTotal, 0)
        self.assertEqual(sample_action.location, 'h')
        self.assertEqual(sample_action.description, 'Jump Ball Bynum vs. Wallace: Tip to World Peace')
        self.assertEqual(sample_action.actionType, 'Jump Ball')
        self.assertEqual(sample_action.subType, '')
        self.assertEqual(sample_action.videoAvailable, 0)
        self.assertEqual(sample_action.actionId, 2)

    def test_playbyplay_action_about_shooting(self):
        sample_action = self.data_scheme.game.actions[2]
        self.assertEqual(sample_action.actionNumber, 2)
        self.assertEqual(sample_action.clock, 'PT11M46.00S')
        self.assertEqual(sample_action.period, 1)
        self.assertEqual(sample_action.teamId, 1610612747)
        self.assertEqual(sample_action.teamTricode, 'LAL')
        self.assertEqual(sample_action.personId, 101115)
        self.assertEqual(sample_action.playerName, 'Bynum')
        self.assertEqual(sample_action.playerNameI, 'A. Bynum')
        self.assertEqual(sample_action.xLegacy, 0)
        self.assertEqual(sample_action.yLegacy, 41)
        self.assertEqual(sample_action.shotDistance, 4)
        self.assertEqual(sample_action.shotResult, 'Missed')
        self.assertEqual(sample_action.isFieldGoal, 1)
        self.assertEqual(sample_action.scoreHome, '')
        self.assertEqual(sample_action.scoreAway, '')
        self.assertEqual(sample_action.pointsTotal, 0)
        self.assertEqual(sample_action.location, 'h')
        self.assertEqual(sample_action.description, 'MISS Bynum 4\' Jump Shot')
        self.assertEqual(sample_action.actionType, 'Missed Shot')
        self.assertEqual(sample_action.subType, 'Jump Shot')
        self.assertEqual(sample_action.videoAvailable, 0)
        self.assertEqual(sample_action.actionId, 3)

    def test_playbyplay_action_about_made_shot(self):
        sample_action = self.data_scheme.game.actions[11]
        self.assertEqual(sample_action.actionNumber, 11)
        self.assertEqual(sample_action.clock, 'PT10M55.00S')
        self.assertEqual(sample_action.period, 1)
        self.assertEqual(sample_action.teamId, 1610612747)
        self.assertEqual(sample_action.teamTricode, 'LAL')
        self.assertEqual(sample_action.personId, 965)
        self.assertEqual(sample_action.playerName, 'Fisher')
        self.assertEqual(sample_action.playerNameI, 'D. Fisher')
        self.assertEqual(sample_action.xLegacy, -168)
        self.assertEqual(sample_action.yLegacy, 201)
        self.assertEqual(sample_action.shotDistance, 26)
        self.assertEqual(sample_action.shotResult, 'Made')
        self.assertEqual(sample_action.isFieldGoal, 1)
        self.assertEqual(sample_action.scoreHome, '3')
        self.assertEqual(sample_action.scoreAway, '0')
        self.assertEqual(sample_action.pointsTotal, 3)
        self.assertEqual(sample_action.location, 'h')
        self.assertEqual(sample_action.description, 'Fisher 26\' 3PT Jump Shot (3 PTS) (Gasol 1 AST)')
        self.assertEqual(sample_action.actionType, 'Made Shot')
        self.assertEqual(sample_action.subType, 'Jump Shot')
        self.assertEqual(sample_action.videoAvailable, 0)
        self.assertEqual(sample_action.actionId, 12)
