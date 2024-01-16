"""
Unittest cases for boxscoresummaryv3 endpoints data scheme
"""
import datetime
from datetime import timezone
import json
from unittest import TestCase

from swish_acquisition.scheme.endpoints import BoxScoreSummaryV3


with open('tests/data/endpoints/boxscoresummaryv3/0040900407.json', 'r') as fp:
    BOXSCORE_SUMMARY_V3_DATA = json.load(fp)


class BoxScoreSummaryV3EndpointSchemeTestCases(TestCase):

    def setUp(self):
        self.data_scheme = BoxScoreSummaryV3.model_validate(BOXSCORE_SUMMARY_V3_DATA)

    def test_box_score_summary_basic_info(self):
        box_score_summary = self.data_scheme.boxScoreSummary
        self.assertEqual(box_score_summary.gameId, '0040900407')
        self.assertEqual(box_score_summary.gameCode, '20100617/BOSLAL')
        self.assertEqual(box_score_summary.gameStatus, 3)
        self.assertEqual(box_score_summary.gameStatusText, 'Final')
        self.assertEqual(box_score_summary.period, 4)
        self.assertEqual(box_score_summary.gameClock, 'PT00M00.00S')
        self.assertEqual(box_score_summary.gameTimeUTC, datetime.datetime(2010, 6, 18, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(box_score_summary.gameEt, datetime.datetime(2010, 6, 17, 21, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(box_score_summary.awayTeamId, 1610612738)
        self.assertEqual(box_score_summary.homeTeamId, 1610612747)
        self.assertEqual(box_score_summary.duration, '2:47')
        self.assertEqual(box_score_summary.attendance, 18997)
        self.assertEqual(box_score_summary.sellout, 1)
        self.assertEqual(box_score_summary.seriesGameNumber, 'Game 7')
        self.assertEqual(box_score_summary.seriesText, 'LAL wins 4-3')
        self.assertEqual(box_score_summary.ifNecessary, False)
        self.assertIsNotNone(box_score_summary.arena)
        self.assertIsInstance(box_score_summary.officials, list)
        self.assertIsNotNone(box_score_summary.broadcasters)
        self.assertIsNotNone(box_score_summary.homeTeam)
        self.assertIsNotNone(box_score_summary.awayTeam)
        self.assertIsNotNone(box_score_summary.lastFiveMeetings)
        self.assertIsNotNone(box_score_summary.pregameCharts)
        self.assertIsNotNone(box_score_summary.postgameCharts)
        self.assertEqual(box_score_summary.videoAvailableFlag, 0)
        self.assertEqual(box_score_summary.ptAvailable, 0)
        self.assertEqual(box_score_summary.ptXYZAvailable, 0)
        self.assertEqual(box_score_summary.whStatus, 1)
        self.assertEqual(box_score_summary.hustleStatus, 1)
        self.assertEqual(box_score_summary.historicalStatus, 0)
        self.assertEqual(box_score_summary.gameSubtype, '')

    def test_arena(self):
        arena = self.data_scheme.boxScoreSummary.arena
        self.assertEqual(arena.arenaId, 137)
        self.assertEqual(arena.arenaName, 'STAPLES Center')
        self.assertEqual(arena.arenaCity, 'Los Angeles')
        self.assertEqual(arena.arenaState, 'CA')
        self.assertEqual(arena.arenaCountry, 'US')
        self.assertEqual(arena.arenaTimezone, 'Pacific')
        self.assertEqual(arena.arenaStreetAddress, '1111 S Figueroa St')
        self.assertEqual(arena.arenaPostalCode, '90015')

    def test_official(self):
        sample_official, *_ = self.data_scheme.boxScoreSummary.officials
        self.assertEqual(sample_official.personId, 1153)
        self.assertEqual(sample_official.name, 'Joe Crawford')
        self.assertEqual(sample_official.nameI, 'J. Crawford')
        self.assertEqual(sample_official.firstName, 'Joe')
        self.assertEqual(sample_official.familyName, 'Crawford')
        self.assertEqual(sample_official.jerseyNum, '17')
        self.assertEqual(sample_official.assignment, '')

    def test_broadcasters(self):
        broadcasters = self.data_scheme.boxScoreSummary.broadcasters
        target_attr_prefixes = (
            'national',
            'nationalRadio',
            'nationalOtt',
            'homeTv',
            'homeRadio',
            'homeOtt',
            'awayTv',
            'awayRadio',
            'awayOtt'
        )
        for prefix in target_attr_prefixes:
            self.assertIsInstance(getattr(broadcasters, f'{prefix}Broadcasters'), list)

        sample_broadcaster, *_ = broadcasters.nationalBroadcasters
        self.assertEqual(sample_broadcaster.broadcasterId, 1)
        self.assertEqual(sample_broadcaster.broadcastDisplay, 'ABC')
        self.assertEqual(sample_broadcaster.broadcasterDisplay, 'ABC')
        self.assertEqual(sample_broadcaster.broadcasterVideoLink, '')
        self.assertEqual(sample_broadcaster.broadcasterTeamId, -1)

    def test_team_basic_info(self):
        sample_team = self.data_scheme.boxScoreSummary.homeTeam
        self.assertEqual(sample_team.teamId, 1610612747)
        self.assertEqual(sample_team.teamName, 'Lakers')
        self.assertEqual(sample_team.teamCity, 'Los Angeles')
        self.assertEqual(sample_team.teamTricode, 'LAL')
        self.assertEqual(sample_team.teamSlug, 'lakers')
        self.assertEqual(sample_team.teamWins, 16)
        self.assertEqual(sample_team.teamLosses, 7)
        self.assertEqual(sample_team.score, 83)
        self.assertEqual(sample_team.inBonus, '')
        self.assertEqual(sample_team.timeoutsRemaining, 1)
        self.assertEqual(sample_team.seed, 1)
        self.assertIsNotNone(sample_team.statistics)
        self.assertIsInstance(sample_team.periods, list)
        self.assertIsInstance(sample_team.players, list)
        self.assertIsInstance(sample_team.inactives, list)

    def test_team_statistics(self):
        statistics = self.data_scheme.boxScoreSummary.homeTeam.statistics
        self.assertEqual(statistics.dummyKey, 'dummyValue')

    def test_team_period_summary(self):
        sample_period, *_ = self.data_scheme.boxScoreSummary.homeTeam.periods
        self.assertEqual(sample_period.period, 1)
        self.assertEqual(sample_period.periodType, 'REGULAR')
        self.assertEqual(sample_period.score, 14)

    def test_team_active_player(self):
        sample_player, *_ = self.data_scheme.boxScoreSummary.homeTeam.players
        self.assertEqual(sample_player.personId, 101115)
        self.assertEqual(sample_player.name, 'Andrew Bynum')
        self.assertEqual(sample_player.nameI, 'A. Bynum')
        self.assertEqual(sample_player.firstName, 'Andrew')
        self.assertEqual(sample_player.familyName, 'Bynum')
        self.assertEqual(sample_player.jerseyNum, '17')

    def test_team_inactive_player(self):
        sample_player, *_ = self.data_scheme.boxScoreSummary.homeTeam.inactives
        self.assertEqual(sample_player.personId, 200747)
        self.assertEqual(sample_player.firstName, 'Adam')
        self.assertEqual(sample_player.familyName, 'Morrison')
        self.assertEqual(sample_player.jerseyNum, '6')

    def test_last_five_meetings_item(self):
        meetings = self.data_scheme.boxScoreSummary.lastFiveMeetings.meetings
        self.assertIsInstance(meetings, list)
        sample_meeting, *_ = meetings
        self.assertEqual(sample_meeting.recencyOrder, 1)
        self.assertEqual(sample_meeting.gameId, '0040900406')
        self.assertEqual(sample_meeting.gameTimeUTC, datetime.datetime(2010, 6, 16, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sample_meeting.gameEt, datetime.datetime(2010, 6, 15, 21, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sample_meeting.gameStatus, 3)
        self.assertEqual(sample_meeting.gameStatusText, 'Final')
        self.assertEqual(sample_meeting.gameClock, 'PT00M00.00S')

        self.assertIsNotNone(sample_meeting.awayTeam)
        self.assertIsNotNone(sample_meeting.homeTeam)
        sample_prev_meeting_team_item = sample_meeting.awayTeam
        self.assertEqual(sample_prev_meeting_team_item.teamId, 1610612738)
        self.assertEqual(sample_prev_meeting_team_item.teamCity, 'Boston')
        self.assertEqual(sample_prev_meeting_team_item.teamName, 'Celtics')
        self.assertEqual(sample_prev_meeting_team_item.teamTricode, 'BOS')
        self.assertEqual(sample_prev_meeting_team_item.teamSlug, 'celtics')
        self.assertEqual(sample_prev_meeting_team_item.score, 67)
        self.assertEqual(sample_prev_meeting_team_item.wins, 15)
        self.assertEqual(sample_prev_meeting_team_item.losses, 8)

    def test_pregame_chart(self):
        pregame_charts = self.data_scheme.boxScoreSummary.pregameCharts
        self.assertIsNotNone(pregame_charts.homeTeam)
        self.assertIsNotNone(pregame_charts.awayTeam)

        sample_team_pregame_chart = pregame_charts.homeTeam
        self.assertEqual(sample_team_pregame_chart.teamId, 1610612747)
        self.assertEqual(sample_team_pregame_chart.teamCity, 'Los Angeles')
        self.assertEqual(sample_team_pregame_chart.teamName, 'Lakers')
        self.assertEqual(sample_team_pregame_chart.teamTricode, 'LAL')
        sample_team_pregame_statistics = sample_team_pregame_chart.statistics
        self.assertEqual(sample_team_pregame_statistics.points, 101.1)
        self.assertEqual(sample_team_pregame_statistics.reboundsTotal, 42.9)
        self.assertEqual(sample_team_pregame_statistics.assists, 19.7)
        self.assertEqual(sample_team_pregame_statistics.steals, 6.7)
        self.assertEqual(sample_team_pregame_statistics.blocks, 6.2)
        self.assertEqual(sample_team_pregame_statistics.turnovers, 11.9)
        self.assertEqual(sample_team_pregame_statistics.fieldGoalsPercentage, 0.46)
        self.assertEqual(sample_team_pregame_statistics.threePointersPercentage, 0.33)
        self.assertEqual(sample_team_pregame_statistics.freeThrowsPercentage, 0.754)
        self.assertEqual(sample_team_pregame_statistics.pointsInThePaint, 41.5)
        self.assertEqual(sample_team_pregame_statistics.pointsSecondChance, 15.3)
        self.assertEqual(sample_team_pregame_statistics.pointsFastBreak, 7.0)
        self.assertEqual(sample_team_pregame_statistics.playerPtsLeaderFirstName, 'Kobe')
        self.assertEqual(sample_team_pregame_statistics.playerPtsLeaderFamilyName, 'Bryant')
        self.assertEqual(sample_team_pregame_statistics.playerPtsLeaderId, 977)
        self.assertEqual(sample_team_pregame_statistics.playerPtsLeaderPts, 28.6)
        self.assertEqual(sample_team_pregame_statistics.playerRebLeaderFirstName, 'Pau')
        self.assertEqual(sample_team_pregame_statistics.playerRebLeaderFamilyName, 'Gasol')
        self.assertEqual(sample_team_pregame_statistics.playerRebLeaderId, 2200)
        self.assertEqual(sample_team_pregame_statistics.playerRebLeaderReb, 11.6)
        self.assertEqual(sample_team_pregame_statistics.playerAstLeaderFirstName, 'Kobe')
        self.assertEqual(sample_team_pregame_statistics.playerAstLeaderFamilyName, 'Bryant')
        self.assertEqual(sample_team_pregame_statistics.playerAstLeaderId, 977)
        self.assertEqual(sample_team_pregame_statistics.playerAstLeaderAst, 3.9)
        self.assertEqual(sample_team_pregame_statistics.playerBlkLeaderFirstName, 'Pau')
        self.assertEqual(sample_team_pregame_statistics.playerBlkLeaderFamilyName, 'Gasol')
        self.assertEqual(sample_team_pregame_statistics.playerBlkLeaderId, 2200)
        self.assertEqual(sample_team_pregame_statistics.playerBlkLeaderBlk, 2.57)

    def test_postgame_chart(self):
        postgame_charts = self.data_scheme.boxScoreSummary.postgameCharts
        self.assertIsNotNone(postgame_charts.homeTeam)
        self.assertIsNotNone(postgame_charts.awayTeam)

        sample_team_postgame_chart = postgame_charts.awayTeam
        self.assertEqual(sample_team_postgame_chart.teamId, 1610612738)
        self.assertEqual(sample_team_postgame_chart.teamCity, 'Boston')
        self.assertEqual(sample_team_postgame_chart.teamName, 'Celtics')
        self.assertEqual(sample_team_postgame_chart.teamTricode, 'BOS')
        sample_team_postgame_statistics = sample_team_postgame_chart.statistics
        self.assertEqual(sample_team_postgame_statistics.points, 79.0)
        self.assertEqual(sample_team_postgame_statistics.reboundsTotal, 40.0)
        self.assertEqual(sample_team_postgame_statistics.assists, 18.0)
        self.assertEqual(sample_team_postgame_statistics.steals, 6.0)
        self.assertEqual(sample_team_postgame_statistics.blocks, 7.0)
        self.assertEqual(sample_team_postgame_statistics.turnovers, 14.0)
        self.assertEqual(sample_team_postgame_statistics.fieldGoalsPercentage, 0.408)
        self.assertEqual(sample_team_postgame_statistics.threePointersPercentage, 0.375)
        self.assertEqual(sample_team_postgame_statistics.freeThrowsPercentage, 0.882)
        self.assertEqual(sample_team_postgame_statistics.pointsInThePaint, 36.0)
        self.assertEqual(sample_team_postgame_statistics.pointsSecondChance, 7.0)
        self.assertEqual(sample_team_postgame_statistics.pointsFastBreak, 6.0)
        self.assertEqual(sample_team_postgame_statistics.biggestLead, 13.0)
        self.assertEqual(sample_team_postgame_statistics.leadChanges, 8.0)
        self.assertEqual(sample_team_postgame_statistics.timesTied, 5.0)
        self.assertEqual(sample_team_postgame_statistics.biggestScoringRun, 11.0)
        self.assertEqual(sample_team_postgame_statistics.turnoversTeam, 1.0)
        self.assertEqual(sample_team_postgame_statistics.turnoversTotal, 15.0)
        self.assertEqual(sample_team_postgame_statistics.reboundsTeam, 6.0)
        self.assertEqual(sample_team_postgame_statistics.pointsFromTurnovers, 14.0)
        self.assertEqual(sample_team_postgame_statistics.benchPoints, 6.0)
        self.assertEqual(sample_team_postgame_statistics.playerPtsLeaderFirstName, 'Paul')
        self.assertEqual(sample_team_postgame_statistics.playerPtsLeaderFamilyName, 'Pierce')
        self.assertEqual(sample_team_postgame_statistics.playerPtsLeaderId, 1718)
        self.assertEqual(sample_team_postgame_statistics.playerPtsLeaderPts, 18.0)
        self.assertEqual(sample_team_postgame_statistics.playerRebLeaderFirstName, 'Paul')
        self.assertEqual(sample_team_postgame_statistics.playerRebLeaderFamilyName, 'Pierce')
        self.assertEqual(sample_team_postgame_statistics.playerRebLeaderId, 1718)
        self.assertEqual(sample_team_postgame_statistics.playerRebLeaderReb, 10.0)
        self.assertEqual(sample_team_postgame_statistics.playerAstLeaderFirstName, 'Rajon')
        self.assertEqual(sample_team_postgame_statistics.playerAstLeaderFamilyName, 'Rondo')

        self.assertEqual(sample_team_postgame_statistics.playerAstLeaderId, 200765)
        self.assertEqual(sample_team_postgame_statistics.playerAstLeaderAst, 10.0)
        self.assertEqual(sample_team_postgame_statistics.playerBlkLeaderFirstName, 'Kevin')
        self.assertEqual(sample_team_postgame_statistics.playerBlkLeaderFamilyName, 'Garnett')
        self.assertEqual(sample_team_postgame_statistics.playerBlkLeaderId, 708)
        self.assertEqual(sample_team_postgame_statistics.playerBlkLeaderBlk, 4.0)
