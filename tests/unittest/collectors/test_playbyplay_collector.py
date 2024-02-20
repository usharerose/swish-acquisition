"""
Unittest cases for Play-by-play data collection
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from swish_acquisition.collectors import PlayByPlayCollector
from tests.utils import get_mocked_response


with open('tests/data/endpoints/playbyplayv3/0040900407.json', 'r') as fp:
    PLAYBYPLAY_V3_DATA = json.load(fp)


class PlayByPlayCollectorTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2010, 6, 17)
        self.game_id = '0040900407'

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.PlayByPlayV3Endpoint._send_api_request')
    def test_run(self, mock_request,
                 mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(PLAYBYPLAY_V3_DATA).encode('utf-8')
        )
        mock_get_object.side_effect = S3Error(
            code='NoSuchKey',
            message='The specified key does not exist.',
            resource='/playbyplay/{year:04d}/{month:02d}/{day:02d}/{game_id}.json'.format(
                year=self.sample_date.year,
                month=self.sample_date.month,
                day=self.sample_date.day,
                game_id=self.game_id
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

        collector = PlayByPlayCollector(
            game_date=self.sample_date,
            game_id=self.game_id
        )
        collector.run()

        mock_upload_object.assert_called_once_with(PLAYBYPLAY_V3_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.PlayByPlayV3Endpoint._send_api_request')
    def test_run_with_local_object(self, mock_request,
                                   mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(PLAYBYPLAY_V3_DATA).encode('utf-8')
        )
        mock_get_object.return_value = PLAYBYPLAY_V3_DATA
        mock_upload_object.return_value = None

        collector = PlayByPlayCollector(
            game_date=self.sample_date,
            game_id=self.game_id
        )
        collector.run()

        self.assertEqual(collector._data_dict, PLAYBYPLAY_V3_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.endpoints.PlayByPlayV3Endpoint._send_api_request')
    def test_run_when_overwritten(self, mock_request, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(PLAYBYPLAY_V3_DATA).encode('utf-8')
        )
        mock_upload_object.return_value = None

        collector = PlayByPlayCollector(
            game_date=self.sample_date,
            game_id=self.game_id
        )
        collector.run(overwritten=True)

        mock_upload_object.assert_called_once_with(PLAYBYPLAY_V3_DATA)
