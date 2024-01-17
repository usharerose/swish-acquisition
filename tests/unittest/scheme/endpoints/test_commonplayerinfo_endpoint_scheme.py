"""
Unittest cases for commonplayerinfo endpoints data scheme
"""
import datetime
import json
from unittest import TestCase

from swish_acquisition.scheme.endpoints import CommonPlayerInfo


with open('tests/data/endpoints/commonplayerinfo/893.json', 'r') as fp:
    COMMON_PLAYER_INFO_DATA = json.load(fp)


class CommonPlayerInfoEndpointSchemeTestCases(TestCase):

    def setUp(self):
        self.data_scheme = CommonPlayerInfo.model_validate(COMMON_PLAYER_INFO_DATA)

    def test_commonplayerinfo_basic_info(self):
        self.assertEqual(self.data_scheme.resource, 'commonplayerinfo')

        actual_player_id_param, actual_league_id_param = self.data_scheme.parameters
        self.assertEqual(actual_player_id_param.PlayerID, 893)
        # since the request of response doesn't input LeagueID param
        self.assertIsNone(actual_league_id_param.LeagueID)

        self.assertIsInstance(self.data_scheme.resultSets, list)

    def test_common_player_info_result_set(self):
        common_player_info_result_set, _, _ = self.data_scheme.resultSets
        self.assertEqual(common_player_info_result_set.name, 'CommonPlayerInfo')
        self.assertIsInstance(common_player_info_result_set.rowSet, list)
        self.assertEqual(len(common_player_info_result_set.rowSet), 1)
        row_set_item, *_ = common_player_info_result_set.rowSet
        self.assertEqual(row_set_item.PERSON_ID, 893)
        self.assertEqual(row_set_item.FIRST_NAME, 'Michael')
        self.assertEqual(row_set_item.LAST_NAME, 'Jordan')
        self.assertEqual(
            row_set_item.DISPLAY_FIRST_LAST,
            f'{row_set_item.FIRST_NAME} {row_set_item.LAST_NAME}'
        )
        self.assertEqual(
            row_set_item.DISPLAY_LAST_COMMA_FIRST,
            f'{row_set_item.LAST_NAME}, {row_set_item.FIRST_NAME}'
        )
        self.assertEqual(row_set_item.DISPLAY_FI_LAST, 'M. Jordan')
        self.assertEqual(row_set_item.PLAYER_SLUG, 'michael-jordan')
        self.assertEqual(row_set_item.BIRTHDATE, datetime.datetime(1963, 2, 17, 0, 0, 0))
        self.assertEqual(row_set_item.SCHOOL, 'North Carolina')
        self.assertEqual(row_set_item.COUNTRY, 'USA')
        self.assertEqual(row_set_item.LAST_AFFILIATION, f'{row_set_item.SCHOOL}/{row_set_item.COUNTRY}')
        self.assertEqual(row_set_item.HEIGHT, '6-6')
        self.assertEqual(row_set_item.WEIGHT, '216')
        self.assertEqual(row_set_item.SEASON_EXP, 15)
        self.assertEqual(row_set_item.JERSEY, '23')
        self.assertEqual(row_set_item.POSITION, 'Guard')
        self.assertEqual(row_set_item.ROSTERSTATUS, 'Inactive')
        self.assertEqual(row_set_item.GAMES_PLAYED_CURRENT_SEASON_FLAG, 'N')
        self.assertEqual(row_set_item.TEAM_ID, 1610612741)
        self.assertEqual(row_set_item.TEAM_NAME, 'Bulls')
        self.assertEqual(row_set_item.TEAM_ABBREVIATION, 'CHI')
        self.assertEqual(row_set_item.TEAM_CODE, 'bulls')
        self.assertEqual(row_set_item.TEAM_CITY, 'Chicago')
        self.assertEqual(row_set_item.PLAYERCODE, 'michael_jordan')
        self.assertEqual(row_set_item.FROM_YEAR, 1984)
        self.assertEqual(row_set_item.TO_YEAR, 2002)
        self.assertEqual(row_set_item.DLEAGUE_FLAG, 'N')
        self.assertEqual(row_set_item.NBA_FLAG, 'Y')
        self.assertEqual(row_set_item.GAMES_PLAYED_FLAG, 'Y')
        self.assertEqual(row_set_item.DRAFT_YEAR, '1984')
        self.assertEqual(row_set_item.DRAFT_ROUND, '1')
        self.assertEqual(row_set_item.DRAFT_NUMBER, '3')
        self.assertEqual(row_set_item.GREATEST_75_FLAG, 'Y')

    def test_player_headline_stats_result_set(self):
        _, player_headline_stats, _ = self.data_scheme.resultSets
        self.assertEqual(player_headline_stats.name, 'PlayerHeadlineStats')
        self.assertIsInstance(player_headline_stats.rowSet, list)
        self.assertEqual(len(player_headline_stats.rowSet), 1)
        row_set_item, *_ = player_headline_stats.rowSet
        self.assertEqual(row_set_item.PLAYER_ID, 893)
        self.assertEqual(row_set_item.PLAYER_NAME, 'Michael Jordan')
        self.assertEqual(row_set_item.TimeFrame, 'career')
        self.assertEqual(row_set_item.PTS, 30.1)
        self.assertEqual(row_set_item.AST, 5.3)
        self.assertEqual(row_set_item.REB, 6.2)
        self.assertEqual(row_set_item.ALL_STAR_APPEARANCES, 13)

    def test_available_seasons_result_set(self):
        _, _, available_seasons = self.data_scheme.resultSets
        self.assertEqual(available_seasons.name, 'AvailableSeasons')
        self.assertIsInstance(available_seasons.rowSet, list)
        sample_row_set_item, *_ = available_seasons.rowSet
        self.assertEqual(sample_row_set_item.SEASON_ID, '21984')
