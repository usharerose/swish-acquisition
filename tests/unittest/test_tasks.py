"""
Celery tasks unittest cases
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from swish_acquisition.celery_app import app
from swish_acquisition.endpoints.base import DATE_FORMAT_V3
from swish_acquisition.tasks import scrape_daily_scoreboard
from tests.utils import get_mocked_response


with open('tests/data/endpoints/scoreboardv3/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)


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
