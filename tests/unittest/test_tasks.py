"""
Celery tasks unittest cases
"""
import datetime
from http import HTTPStatus
import json
from typing import Any
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from swish_acquisition.celery_app import app
from swish_acquisition.endpoints.base import DATE_FORMAT_V3
from swish_acquisition.tasks import (
    scrape_daily_scoreboard,
    scrape_single_game_series
)
from tests.utils import get_mocked_response


with open('tests/data/endpoints/boxscoresummaryv3/0040900407.json', 'r') as fp:
    BOXSCORE_SUMMARY_V3_DATA = json.load(fp)
with open('tests/data/endpoints/commonplayerinfo/893.json', 'r') as fp:
    COMMON_PLAYER_INFO_DATA = json.load(fp)
with open('tests/data/endpoints/playbyplayv3/0040900407.json', 'r') as fp:
    PLAYBYPLAY_V3_DATA = json.load(fp)
with open('tests/data/endpoints/scoreboardv3/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)
with open('tests/data/endpoints/teamdetails/1610612741.json', 'r') as fp:
    TEAM_DETAILS_DATA = json.load(fp)


class TasksTestCases(TestCase):

    def setUp(self) -> None:
        self.origin_task_always_eager = app.conf.task_always_eager
        app.conf.task_always_eager = True

    def tearDown(self) -> None:
        app.conf.task_always_eager = self.origin_task_always_eager

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.ScoreboardV3Endpoint._send_api_request')
    def test_scrape_daily_scoreboard(self, mock_request,
                                     mock_get_object, mock_upload_object):
        sample_game_date = datetime.date(2022, 5, 29)
        sample_league_id = '00'
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        mock_get_object.side_effect = S3Error(
            code='NoSuchKey',
            message='The specified key does not exist.',
            resource='/scoreboard/{year:04d}/{month:02d}/{day:02d}.json'.format(
                year=sample_game_date.year,
                month=sample_game_date.month,
                day=sample_game_date.day
            ),
            request_id='MOCKREQUESTID',
            host_id='mockhostid',
            response=BaseHTTPResponse(
                status=HTTPStatus.BAD_REQUEST.value,
                version=1,
                reason=None,
                decode_content=False,
                request_url=None
            )
        )
        mock_upload_object.return_value = None

        scrape_daily_scoreboard.delay(
            game_date=sample_game_date.strftime(DATE_FORMAT_V3),
            league_id=sample_league_id
        )

        mock_upload_object.assert_called_once_with(SCOREBOARD_V3_DATA)

    @patch('swish_acquisition.tasks.request_interval')
    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.PlayByPlayV3Endpoint._send_api_request')
    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    @patch('swish_acquisition.endpoints.TeamDetailsEndpoint._send_api_request')
    @patch('swish_acquisition.endpoints.BoxScoreSummaryV3Endpoint._send_api_request')
    def test_scrape_single_game_series(self, mock_boxscore_summary_request,
                                       mock_teamdetails_request,
                                       mock_commonplayerinfo_request,
                                       mock_playbyplay_request,
                                       mock_get_object, mock_upload_object,
                                       mock_request_interval):
        sample_game_date = datetime.date(2022, 5, 29)
        sample_game_id = '0040900407'

        def _get_side_effect_generator(ret: Any, count: int):
            for _ in range(count):
                yield ret

        game_count = 1
        team_count = 2
        away_player_count = 15
        home_player_count = 13
        expected_call_count = (game_count + team_count +
                               away_player_count + home_player_count +
                               game_count)

        mock_boxscore_summary_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(BOXSCORE_SUMMARY_V3_DATA).encode('utf-8')
        )
        # would be called for each team
        mock_teamdetails_request.side_effect = _get_side_effect_generator(
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
            ),
            team_count
        )
        # would be called for every active & inactive players from each team
        mock_commonplayerinfo_request.side_effect = _get_side_effect_generator(
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
            ),
            away_player_count + home_player_count
        )
        mock_playbyplay_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(PLAYBYPLAY_V3_DATA).encode('utf-8')
        )

        mock_get_object.side_effect = _get_side_effect_generator(
            S3Error(
                code='NoSuchKey',
                message='The specified key does not exist.',
                resource='mock_resource.json',
                request_id='MOCKREQUESTID',
                host_id='mockhostid',
                response=BaseHTTPResponse(
                    status=HTTPStatus.BAD_REQUEST.value,
                    version=1,
                    reason=None,
                    decode_content=False,
                    request_url=None
                )
            ),
            expected_call_count
        )
        mock_upload_object.side_effect = _get_side_effect_generator(
            None, expected_call_count
        )
        # would be called after each commonplayerinfo & teamdetals request
        mock_request_interval.side_effect = _get_side_effect_generator(
            None, team_count + away_player_count + home_player_count
        )

        scrape_single_game_series.delay(
            game_date=sample_game_date.strftime(DATE_FORMAT_V3),
            game_id=sample_game_id
        )

        self.assertEqual(mock_upload_object.call_count, expected_call_count)
