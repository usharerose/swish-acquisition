"""
Unittest cases for scoreboardv3 endpoint data acquisition
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

from swish_acquisition.scoreboardv3 import ScoreboardV3Endpoint


with open('tests/data/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)


class ScoreboardV3EndpointTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2022, 5, 29)
        self.league_id = '00'

    @patch('swish_acquisition.scoreboardv3.ScoreboardV3Endpoint._send_api_request')
    def test_request(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'league_id': self.league_id
        }
        endpoint = ScoreboardV3Endpoint(**params)
        response = endpoint.request()

        self.assertEqual(response.status_code, HTTPStatus.OK)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, SCOREBOARD_V3_DATA)

    @patch('swish_acquisition.scoreboardv3.ScoreboardV3Endpoint._send_api_request')
    def test_get_data(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'league_id': self.league_id
        }
        endpoint = ScoreboardV3Endpoint(**params)
        dm = endpoint.get_data()

        self.assertEqual(dm.scoreboard.gameDate, self.sample_date)
        self.assertEqual(dm.scoreboard.leagueId, '00')

    @patch('swish_acquisition.scoreboardv3.ScoreboardV3Endpoint._send_api_request')
    def test_request_failed(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'league_id': self.league_id
        }
        endpoint = ScoreboardV3Endpoint(**params)
        response = endpoint.request()

        self.assertIsNone(response)

    @patch('swish_acquisition.scoreboardv3.ScoreboardV3Endpoint._send_api_request')
    def test_get_data_with_failed_request(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'league_id': self.league_id
        }
        endpoint = ScoreboardV3Endpoint(**params)
        dm = endpoint.get_data()

        self.assertIsNone(dm)
