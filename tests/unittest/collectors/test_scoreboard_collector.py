"""
Unittest cases for scoreboard data collection
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from tests.utils import get_mocked_response

from swish_acquisition.collectors import ScoreboardCollector


with open('tests/data/endpoints/scoreboardv3/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)


class ScoreboardCollectorTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2022, 5, 29)
        self.league_id = '00'

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.ScoreboardV3Endpoint._send_api_request')
    def test_run(self, mock_request,
                 mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        mock_get_object.side_effect = S3Error(
            code='NoSuchKey',
            message='The specified key does not exist.',
            resource='/scoreboard/{year:04d}/{month:02d}/{day:02d}.json'.format(
                year=self.sample_date.year,
                month=self.sample_date.month,
                day=self.sample_date.day
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

        collector = ScoreboardCollector(game_date=self.sample_date, league_id=self.league_id)
        collector.run()

        mock_upload_object.assert_called_once_with(SCOREBOARD_V3_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.ScoreboardV3Endpoint._send_api_request')
    def test_run_with_local_object(self, mock_request,
                                   mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        mock_get_object.return_value = SCOREBOARD_V3_DATA
        mock_upload_object.return_value = None

        collector = ScoreboardCollector(game_date=self.sample_date, league_id=self.league_id)
        collector.run()

        self.assertEqual(collector._data_dict, SCOREBOARD_V3_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.endpoints.ScoreboardV3Endpoint._send_api_request')
    def test_run_when_overwritten(self, mock_request, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        mock_upload_object.return_value = None

        collector = ScoreboardCollector(game_date=self.sample_date, league_id=self.league_id)
        collector.run(overwritten=True)

        mock_upload_object.assert_called_once_with(SCOREBOARD_V3_DATA)
