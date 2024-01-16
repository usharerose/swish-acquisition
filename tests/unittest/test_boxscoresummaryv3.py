"""
Unittest cases for boxscoresummaryv3 endpoint data acquisition
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

from swish_acquisition.boxscoresummaryv3 import BoxScoreSummaryV3Endpoint


with open('tests/data/endpoints/boxscoresummaryv3/0040900407.json', 'r') as fp:
    BOXSCORE_SUMMARY_V3_DATA = json.load(fp)


class BoxScoreSummaryV3EndpointTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2022, 5, 29)
        self.sample_game_id = '0040900407'

    @patch('swish_acquisition.boxscoresummaryv3.BoxScoreSummaryV3Endpoint._send_api_request')
    def test_request(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(BOXSCORE_SUMMARY_V3_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'game_id': self.sample_game_id
        }
        endpoint = BoxScoreSummaryV3Endpoint(**params)
        response = endpoint.request()

        self.assertEqual(response.status_code, HTTPStatus.OK)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, BOXSCORE_SUMMARY_V3_DATA)

    @patch('swish_acquisition.boxscoresummaryv3.BoxScoreSummaryV3Endpoint._send_api_request')
    def test_get_data(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(BOXSCORE_SUMMARY_V3_DATA).encode('utf-8')
        )
        params = {
            'game_date': self.sample_date,
            'game_id': self.sample_game_id
        }
        endpoint = BoxScoreSummaryV3Endpoint(**params)
        dm = endpoint.get_data()

        self.assertEqual(dm.boxScoreSummary.gameId, self.sample_game_id)

    @patch('swish_acquisition.boxscoresummaryv3.BoxScoreSummaryV3Endpoint._send_api_request')
    def test_request_failed(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'game_id': self.sample_game_id
        }
        endpoint = BoxScoreSummaryV3Endpoint(**params)
        response = endpoint.request()

        self.assertIsNone(response)

    @patch('swish_acquisition.boxscoresummaryv3.BoxScoreSummaryV3Endpoint._send_api_request')
    def test_get_data_with_failed_request(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        params = {
            'game_date': self.sample_date,
            'game_id': self.sample_game_id
        }
        endpoint = BoxScoreSummaryV3Endpoint(**params)
        dm = endpoint.get_data()

        self.assertIsNone(dm)
