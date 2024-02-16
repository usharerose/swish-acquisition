"""
Basis components for collecting endpoint raw data
"""
from http import HTTPStatus
import json
import logging
from typing import cast, Dict, Optional, Type
from urllib.parse import urljoin

from pydantic import BaseModel
import requests
from requests import ConnectTimeout, ReadTimeout, Response


logger = logging.getLogger(__name__)


NBA_STATS_BASE_URL = 'https://stats.nba.com/stats/'
DATE_FORMAT_V3 = '%Y-%m-%d'
NBA_STATS_REQUEST_HEADERS = {
    'host': 'stats.nba.com',
    'origin': 'https://www.nba.com',
    'referer': 'https://www.nba.com/',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}
DEFAULT_TIMEOUT = 5


class Endpoint:

    BASE_URL: str = NBA_STATS_BASE_URL
    DATA_MODEL: Optional[Type[BaseModel]] = None
    ENDPOINT: Optional[str] = None
    HEADERS = NBA_STATS_REQUEST_HEADERS
    TIMEOUT: int = DEFAULT_TIMEOUT

    def __init__(self, *args, **kwargs):
        self._validate_endpoint_arguments()
        self._url = urljoin(self.BASE_URL, self.ENDPOINT)
        self._data_dict: Dict = {}
        self._has_called_remote = False

    def _validate_endpoint_arguments(self) -> None:
        for item in (self.DATA_MODEL, self.ENDPOINT):
            if item is None:
                raise

    def get_params(self) -> Dict:
        raise NotImplementedError

    def request(self) -> Optional[Response]:
        params = self.get_params()
        request_args = {
            'url': self._url,
            'params': params,
            'headers': self.HEADERS,
            'timeout': self.TIMEOUT
        }
        response = None
        # TODO: add try-catch and logging when raise exceptions
        try:
            response = self._send_api_request(**request_args)
        except (ConnectTimeout, ReadTimeout) as e:  # NOQA
            pass
        if response and response.status_code != HTTPStatus.OK:
            response = None
        self._has_called_remote = True
        return response

    # which is easy to be mocked
    @staticmethod
    def _send_api_request(*args, **kwargs) -> Response:
        return requests.get(*args, **kwargs)

    def get_data(self, overwritten: bool = False) -> Optional[BaseModel]:
        data_dict = self.get_dict(overwritten)
        if not data_dict or self.DATA_MODEL is None:
            return None
        return cast(BaseModel, self.DATA_MODEL).model_validate(data_dict)

    def get_dict(self, overwritten: bool = False) -> Dict:
        if not self._has_called_remote or overwritten:
            response = self.request()
            data_dict = {} if response is None else json.loads(response.content.decode('utf-8'))
            self._set_data_dict(data_dict)
        return self._data_dict

    def _set_data_dict(self, data_dict: Dict) -> None:
        assert isinstance(data_dict, dict)
        self._data_dict = data_dict
