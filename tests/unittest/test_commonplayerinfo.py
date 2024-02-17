"""
Unittest cases for commonplayerinfo endpoint data acquisition
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

from swish_acquisition.endpoints.commonplayerinfo import CommonPlayerInfoEndpoint


with open('tests/data/endpoints/commonplayerinfo/893.json', 'r') as fp:
    COMMON_PLAYER_INFO_DATA = json.load(fp)


class CommonPlayerInfoEndpointTestCases(TestCase):

    def setUp(self):
        self.sample_date = datetime.date(2003, 4, 16)
        self.sample_player_id = 893
        self.sample_params = {
            'game_date': self.sample_date,
            'player_id': self.sample_player_id
        }

    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_request(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
        )
        endpoint = CommonPlayerInfoEndpoint(**self.sample_params)
        response = endpoint.request()

        self.assertEqual(response.status_code, HTTPStatus.OK)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, COMMON_PLAYER_INFO_DATA)

    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_get_data(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(COMMON_PLAYER_INFO_DATA).encode('utf-8')
        )
        endpoint = CommonPlayerInfoEndpoint(**self.sample_params)
        dm = endpoint.get_data()

        common_player_info_result_set, _, _ = dm.resultSets
        common_player_info, *_ = common_player_info_result_set.rowSet
        self.assertEqual(common_player_info.PERSON_ID, self.sample_player_id)

    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_request_failed(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        endpoint = CommonPlayerInfoEndpoint(**self.sample_params)
        response = endpoint.request()

        self.assertIsNone(response)

    @patch('swish_acquisition.endpoints.CommonPlayerInfoEndpoint._send_api_request')
    def test_get_data_with_failed_request(self, mock_request):
        mock_request.return_value = get_mocked_error_response()
        endpoint = CommonPlayerInfoEndpoint(**self.sample_params)
        dm = endpoint.get_data()

        self.assertIsNone(dm)
