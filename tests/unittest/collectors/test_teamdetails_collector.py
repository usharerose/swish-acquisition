"""
Unittest cases for Team Details data collection
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch
from urllib3.response import BaseHTTPResponse

from minio import S3Error

from swish_acquisition.collectors import TeamDetailsCollector
from tests.utils import get_mocked_response


with open('tests/data/endpoints/teamdetails/1610612741.json', 'r') as fp:
    TEAM_DETAILS_DATA = json.load(fp)


class TeamDetailsCollectorTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(1998, 6, 14)
        self.team_id = '1610612741'

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.TeamDetailsEndpoint._send_api_request')
    def test_run(self, mock_request,
                 mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
        )
        mock_get_object.side_effect = S3Error(
            code='NoSuchKey',
            message='The specified key does not exist.',
            resource='/teamdetails/{team_id}.json'.format(
                team_id=self.team_id
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

        collector = TeamDetailsCollector(game_date=self.sample_date, team_id=self.team_id)
        collector.run()

        mock_upload_object.assert_called_once_with(TEAM_DETAILS_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.s3.get_s3_object_data')
    @patch('swish_acquisition.endpoints.TeamDetailsEndpoint._send_api_request')
    def test_run_with_local_object(self, mock_request,
                                   mock_get_object, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
        )
        mock_get_object.return_value = TEAM_DETAILS_DATA
        mock_upload_object.return_value = None

        collector = TeamDetailsCollector(game_date=self.sample_date, team_id=self.team_id)
        collector.run()

        self.assertEqual(collector._data_dict, TEAM_DETAILS_DATA)

    @patch('swish_acquisition.s3.S3MixIn.upload_to_s3')
    @patch('swish_acquisition.endpoints.TeamDetailsEndpoint._send_api_request')
    def test_run_when_overwritten(self, mock_request, mock_upload_object):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
        )
        mock_upload_object.return_value = None

        collector = TeamDetailsCollector(game_date=self.sample_date, team_id=self.team_id)
        collector.run(overwritten=True)

        mock_upload_object.assert_called_once_with(TEAM_DETAILS_DATA)
