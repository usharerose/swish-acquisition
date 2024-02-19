"""
Unittest cases for Common Player Info data collection
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from swish_acquisition.collectors import CommonPlayerInfoCollector
from tests.utils import get_mocked_response


with open('tests/data/endpoints/commonplayerinfo/893.json', 'r') as fp:
    COMMON_PLAYER_INFO_DATA = json.load(fp)


class CommonPlayerInfoCollectorTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2003, 4, 16)
        self.player_id = 893

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_run(self, mock_request,
                 mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
        )
        mock_get_object.side_effect = S3Error(
            code='NoSuchKey',
            message='The specified key does not exist.',
            resource='/commonplayerinfo/{player_id}.json'.format(
                player_id=self.player_id
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

        collector = CommonPlayerInfoCollector(
            game_date=self.sample_date,
            player_id=self.player_id
        )
        collector.run()

        mock_upload_object.assert_called_once_with(COMMON_PLAYER_INFO_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_run_with_local_object(self, mock_request,
                                   mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
        )
        mock_get_object.return_value = COMMON_PLAYER_INFO_DATA
        mock_upload_object.return_value = None

        collector = CommonPlayerInfoCollector(
            game_date=self.sample_date,
            player_id=self.player_id
        )
        collector.run()

        self.assertEqual(collector._data_dict, COMMON_PLAYER_INFO_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_run_when_overwritten(self, mock_request, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
        )
        mock_upload_object.return_value = None

        collector = CommonPlayerInfoCollector(
            game_date=self.sample_date,
            player_id=self.player_id
        )
        collector.run(overwritten=True)

        mock_upload_object.assert_called_once_with(COMMON_PLAYER_INFO_DATA)
