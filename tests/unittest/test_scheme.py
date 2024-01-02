"""
Unittest cases for NBA Stats endpoints data scheme
"""
import datetime
from datetime import timezone
import json
from unittest import TestCase

from swish_acquisition.scheme import ScoreboardV3


with open('tests/data/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)


class ScoreboardV3TestCases(TestCase):

    def setUp(self):
        self.data_scheme = ScoreboardV3.model_validate(SCOREBOARD_V3_DATA)

    def test_meta(self):
        meta = self.data_scheme.meta
        self.assertEqual(meta.version, 1)
        self.assertEqual(meta.request, 'http://nba.cloud/league/00/2022/05/29/scoreboard?Format=json')

    def test_scoreboard_basic_info(self):
        scoreboard = self.data_scheme.scoreboard
        self.assertEqual(scoreboard.gameDate, datetime.date(2022, 5, 29))
        self.assertEqual(scoreboard.leagueId, '00')
        self.assertEqual(scoreboard.leagueName, 'National Basketball Association')
        self.assertIsInstance(scoreboard.games, list)

    def test_scoreboard_game_basic_info(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        self.assertEqual(sample_game.gameId, '0042100307')
        self.assertEqual(sample_game.gameCode, '20220529/BOSMIA')
        self.assertEqual(sample_game.gameStatus, 3)
        self.assertEqual(sample_game.gameStatusText, 'Final')
        self.assertEqual(sample_game.period, 4)
        self.assertEqual(sample_game.regulationPeriods, 4)
        self.assertEqual(sample_game.gameClock, '')
        self.assertEqual(sample_game.gameTimeUTC, datetime.datetime(2022, 5, 30, 0, 30, 0, tzinfo=timezone.utc))
        self.assertEqual(sample_game.gameEt, datetime.datetime(2022, 5, 29, 20, 30, 0, tzinfo=timezone.utc))
        self.assertEqual(sample_game.seriesGameNumber, 'Game 7')
        self.assertEqual(sample_game.seriesText, 'BOS wins 4-3')
        self.assertEqual(sample_game.seriesConference, 'East')
        self.assertEqual(sample_game.poRoundDesc, 'Conf. Finals')
        self.assertEqual(sample_game.ifNecessary, False)
        self.assertEqual(sample_game.gameSubtype, '')

        self.assertIsNotNone(sample_game.gameLeaders)
        self.assertIsNotNone(sample_game.teamLeaders)
        self.assertIsNotNone(sample_game.broadcasters)
        self.assertIsNotNone(sample_game.homeTeam)
        self.assertIsNotNone(sample_game.awayTeam)

    def test_scoreboard_game_leader(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        sample_game_leaders = sample_game.gameLeaders
        self.assertIsNotNone(sample_game_leaders.homeLeaders)
        self.assertIsNotNone(sample_game_leaders.awayLeaders)

        sample_game_leader = sample_game_leaders.homeLeaders
        self.assertEqual(sample_game_leader.personId, 202710)
        self.assertEqual(sample_game_leader.name, 'Jimmy Butler')
        self.assertEqual(sample_game_leader.playerSlug, 'jimmy-butler')
        self.assertEqual(sample_game_leader.jerseyNum, '22')
        self.assertEqual(sample_game_leader.position, 'F')
        self.assertEqual(sample_game_leader.teamTricode, 'MIA')
        self.assertEqual(sample_game_leader.points, 35)
        self.assertEqual(sample_game_leader.rebounds, 9)
        self.assertEqual(sample_game_leader.assists, 1)

    def test_scoreboard_team_leader(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        sample_team_leaders = sample_game.teamLeaders
        self.assertIsNotNone(sample_team_leaders.homeLeaders)
        self.assertIsNotNone(sample_team_leaders.awayLeaders)

        sample_team_leader = sample_team_leaders.homeLeaders
        self.assertEqual(sample_team_leader.personId, 202710)
        self.assertEqual(sample_team_leader.name, 'Jimmy Butler')
        self.assertEqual(sample_team_leader.playerSlug, 'jimmy-butler')
        self.assertEqual(sample_team_leader.jerseyNum, '22')
        self.assertEqual(sample_team_leader.position, 'F')
        self.assertEqual(sample_team_leader.teamTricode, 'MIA')
        self.assertEqual(sample_team_leader.points, 27.4)
        self.assertEqual(sample_team_leader.rebounds, 7.4)
        self.assertEqual(sample_team_leader.assists, 4.6)

    def test_scoreboard_broadcasters(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        sample_broadcasters = sample_game.broadcasters
        self.assertIsNotNone(sample_broadcasters.nationalBroadcasters)
        self.assertIsNotNone(sample_broadcasters.nationalRadioBroadcasters)
        self.assertIsNotNone(sample_broadcasters.nationalOttBroadcasters)
        self.assertIsNotNone(sample_broadcasters.homeTvBroadcasters)
        self.assertIsNotNone(sample_broadcasters.homeRadioBroadcasters)
        self.assertIsNotNone(sample_broadcasters.homeOttBroadcasters)
        self.assertIsNotNone(sample_broadcasters.awayTvBroadcasters)
        self.assertIsNotNone(sample_broadcasters.awayRadioBroadcasters)
        self.assertIsNotNone(sample_broadcasters.awayOttBroadcasters)

        sample_broadcaster, *_ = sample_broadcasters.awayRadioBroadcasters
        self.assertEqual(sample_broadcaster.broadcasterId, 1471)
        self.assertEqual(sample_broadcaster.broadcastDisplay, 'WBZ-FM')
        self.assertEqual(sample_broadcaster.broadcasterTeamId, 1610612738)

    def test_scoreboard_team_basic_info(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        self.assertIsNotNone(sample_game.homeTeam)
        self.assertIsNotNone(sample_game.awayTeam)

        sample_team = sample_game.homeTeam
        self.assertEqual(sample_team.teamId, 1610612748)
        self.assertEqual(sample_team.teamName, 'Heat')
        self.assertEqual(sample_team.teamCity, 'Miami')
        self.assertEqual(sample_team.teamTricode, 'MIA')
        self.assertEqual(sample_team.teamSlug, 'heat')
        self.assertEqual(sample_team.wins, 3)
        self.assertEqual(sample_team.losses, 4)
        self.assertEqual(sample_team.score, 96)
        self.assertEqual(sample_team.seed, 1)
        self.assertIsNone(sample_team.inBonus)
        self.assertEqual(sample_team.timeoutsRemaining, 0)
        self.assertIsNotNone(sample_team.periods, list)

    def test_scoreboard_period_item(self):
        sample_game, *_ = self.data_scheme.scoreboard.games
        sample_periods = sample_game.homeTeam.periods

        self.assertEqual(len(sample_periods), 4)
        sample_period, *_ = sample_periods
        self.assertEqual(sample_period.period, 1)
        self.assertEqual(sample_period.periodType, 'REGULAR')
        self.assertEqual(sample_period.score, 17)
