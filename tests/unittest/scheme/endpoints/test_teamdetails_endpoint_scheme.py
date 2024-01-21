"""
Unittest cases for teamdetails endpoints data scheme
"""
import json
from unittest import TestCase

from swish_acquisition.scheme.endpoints import TeamDetails


with open('tests/data/endpoints/teamdetails/1610612741.json', 'r') as fp:
    TEAM_DETAILS_DATA = json.load(fp)


class TeamDetailsEndpointSchemeTestCases(TestCase):

    def setUp(self):
        self.data_scheme = TeamDetails.model_validate(TEAM_DETAILS_DATA)

    def test_teamdetails_basic_info(self):
        self.assertEqual(self.data_scheme.resource, 'teamdetails')

        actual_team_id_param = self.data_scheme.parameters
        self.assertEqual(actual_team_id_param.TeamID, 1610612741)

        self.assertIsInstance(self.data_scheme.resultSets, list)

    def test_team_background_result_set(self):
        team_background_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_background_result_set.name, 'TeamBackground')
        self.assertIsInstance(team_background_result_set.rowSet, list)
        self.assertEqual(len(team_background_result_set.rowSet), 1)
        row_set_item, *_ = team_background_result_set.rowSet
        self.assertEqual(row_set_item.TEAM_ID, 1610612741)
        self.assertEqual(row_set_item.ABBREVIATION, 'CHI')
        self.assertEqual(row_set_item.NICKNAME, 'Bulls')
        self.assertEqual(row_set_item.YEARFOUNDED, 1966)
        self.assertEqual(row_set_item.CITY, 'Chicago')
        self.assertEqual(row_set_item.ARENA, 'United Center')
        self.assertEqual(row_set_item.ARENACAPACITY, '21711')
        self.assertEqual(row_set_item.OWNER, 'Michael Reinsdorf')
        self.assertEqual(row_set_item.GENERALMANAGER, 'Arturas Karnisovas')
        self.assertEqual(row_set_item.HEADCOACH, 'Billy Donovan')
        self.assertEqual(row_set_item.DLEAGUEAFFILIATION, 'Windy City Bulls')

    def test_team_history_result_set(self):
        _, team_history_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_history_result_set.name, 'TeamHistory')
        self.assertIsInstance(team_history_result_set.rowSet, list)
        # there is only one history piece for the sample data
        row_set_item, *_ = team_history_result_set.rowSet
        self.assertEqual(row_set_item.TEAM_ID, 1610612741)
        self.assertEqual(row_set_item.CITY, 'Chicago')
        self.assertEqual(row_set_item.NICKNAME, 'Bulls')
        self.assertEqual(row_set_item.YEARFOUNDED, 1966)
        self.assertEqual(row_set_item.YEARACTIVETILL, 2023)

    def test_team_social_sites_result_set(self):
        _, _, team_social_sites_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_social_sites_result_set.name, 'TeamSocialSites')
        self.assertIsInstance(team_social_sites_result_set.rowSet, list)
        facebook_item, instagram_item, twitter_item = team_social_sites_result_set.rowSet
        self.assertEqual(facebook_item.ACCOUNTTYPE, 'Facebook')
        self.assertEqual(facebook_item.WEBSITE_LINK, 'https://www.facebook.com/chicagobulls')
        self.assertEqual(instagram_item.ACCOUNTTYPE, 'Instagram')
        self.assertEqual(instagram_item.WEBSITE_LINK, 'https://instagram.com/chicagobulls')
        self.assertEqual(twitter_item.ACCOUNTTYPE, 'Twitter')
        self.assertEqual(twitter_item.WEBSITE_LINK, 'https://twitter.com/chicagobulls')

    def test_team_awards_championships_result_set(self):
        _, _, _, team_awards_championships_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_awards_championships_result_set.name, 'TeamAwardsChampionships')
        self.assertIsInstance(team_awards_championships_result_set.rowSet, list)
        sample_row_set_item, *_ = team_awards_championships_result_set.rowSet
        self.assertEqual(sample_row_set_item.YEARAWARDED, 1991)
        self.assertEqual(sample_row_set_item.OPPOSITETEAM, 'Los Angeles Lakers')

    def test_team_awards_conf_result_set(self):
        _, _, _, _, team_awards_conf_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_awards_conf_result_set.name, 'TeamAwardsConf')
        self.assertIsInstance(team_awards_conf_result_set.rowSet, list)
        sample_row_set_item, *_ = team_awards_conf_result_set.rowSet
        self.assertEqual(sample_row_set_item.YEARAWARDED, 1991)
        self.assertEqual(sample_row_set_item.OPPOSITETEAM, None)

    def test_team_awards_div_result_set(self):
        _, _, _, _, _, team_awards_div_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_awards_div_result_set.name, 'TeamAwardsDiv')
        self.assertIsInstance(team_awards_div_result_set.rowSet, list)
        sample_row_set_item, *_ = team_awards_div_result_set.rowSet
        self.assertEqual(sample_row_set_item.YEARAWARDED, 1975)
        self.assertEqual(sample_row_set_item.OPPOSITETEAM, None)

    def test_team_hall_of_fame_result_set(self):
        _, _, _, _, _, _, team_hall_of_fame_result_set, *_ = self.data_scheme.resultSets
        self.assertEqual(team_hall_of_fame_result_set.name, 'TeamHof')
        self.assertIsInstance(team_hall_of_fame_result_set.rowSet, list)
        sample_row_set_item, *_ = team_hall_of_fame_result_set.rowSet
        self.assertEqual(sample_row_set_item.PLAYERID, 2548)
        self.assertEqual(sample_row_set_item.PLAYER, 'Dwyane Wade')
        self.assertEqual(sample_row_set_item.POSITION, 'G')
        self.assertEqual(sample_row_set_item.JERSEY, None)
        self.assertEqual(sample_row_set_item.SEASONSWITHTEAM, '2016-2017')
        self.assertEqual(sample_row_set_item.YEAR, 2023)

    def test_team_retired_result_set(self):
        *_, team_retired_result_set = self.data_scheme.resultSets
        self.assertEqual(team_retired_result_set.name, 'TeamRetired')
        self.assertIsInstance(team_retired_result_set.rowSet, list)
        sample_row_set_item, *_ = team_retired_result_set.rowSet
        self.assertEqual(sample_row_set_item.PLAYERID, None)
        self.assertEqual(sample_row_set_item.PLAYER, 'Johnny Kerr')
        self.assertEqual(sample_row_set_item.POSITION, 'Coach, Business Manager, Broadcaster')
        self.assertEqual(sample_row_set_item.JERSEY, '')
        self.assertEqual(sample_row_set_item.SEASONSWITHTEAM, '1966-2009')
        self.assertEqual(sample_row_set_item.YEAR, 2009)
