"""
Unittest cases for teamdetails endpoint data acquisition
"""
import datetime
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from tests.utils import (
    get_mocked_error_response,
    get_mocked_response
)

from swish_acquisition.teamdetails import TeamDetailsEndpoint


with open('tests/data/endpoints/teamdetails/1610612741.json', 'r') as fp:
    TEAM_DETAILS_DATA = json.load(fp)


class TeamDetailsEndpointTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2022, 5, 29)
        self.sample_team_id = 1610612741

    @patch('swish_acquisition.teamdetails.TeamDetailsEndpoint._send_api_request')
    def test_request(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'team_id': self.sample_team_id
        }
        endpoint = TeamDetailsEndpoint(**params)
        response = endpoint.request()

        self.assertEqual(response.status_code, HTTPStatus.OK)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, TEAM_DETAILS_DATA)

    @patch('swish_acquisition.teamdetails.TeamDetailsEndpoint._send_api_request')
    def test_get_data(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(TEAM_DETAILS_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'team_id': self.sample_team_id
        }
        endpoint = TeamDetailsEndpoint(**params)
        dm = endpoint.get_data()

        team_background_result_set, *_ = dm.resultSets
        team_background, *_ = team_background_result_set.rowSet
        self.assertEqual(team_background.TEAM_ID, self.sample_team_id)

    @patch('swish_acquisition.teamdetails.TeamDetailsEndpoint._send_api_request')
    def test_request_failed(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'team_id': self.sample_team_id
        }
        endpoint = TeamDetailsEndpoint(**params)
        response = endpoint.request()

        self.assertIsNone(response)

    @patch('swish_acquisition.teamdetails.TeamDetailsEndpoint._send_api_request')
    def test_get_data_with_failed_request(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'team_id': self.sample_team_id
        }
        endpoint = TeamDetailsEndpoint(**params)
        dm = endpoint.get_data()

        self.assertIsNone(dm)
