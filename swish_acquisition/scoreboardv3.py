"""
Collect scoreboardv3 endpoint data
"""
import datetime
from http import HTTPStatus
import json
from urllib.parse import urljoin
from typing import Dict, Optional

from pydantic import BaseModel
import requests
from requests import ConnectTimeout, ReadTimeout, Response

from swish_acquisition.scheme import ScoreboardV3


BASE_URL = 'https://stats.nba.com/stats/'
ENDPOINT = 'scoreboardv3'
DATE_FORMAT_V3 = '%Y-%m-%d'
HEADERS = {
    'host': 'stats.nba.com',
    'origin': 'https://www.nba.com',
    'referer': 'https://www.nba.com/',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}
TIMEOUT = 5


class ScoreboardV3Endpoint:

    def __init__(self, game_date: datetime.date, league_id: str):
        self._url = urljoin(BASE_URL, ENDPOINT)
        self._game_date = game_date
        self._league_id = league_id
        self._response: Optional[Response] = None

    @property
    def params(self) -> Dict:
        return {
            'GameDate': self._game_date.strftime(DATE_FORMAT_V3),
            'LeagueID': self._league_id
        }

    @property
    def url(self) -> str:
        return self._url

    def request(self) -> Optional[Response]:
        request_args = {
            'url': self.url,
            'params': self.params,
            'headers': HEADERS,
            'timeout': TIMEOUT
        }
        response = None
        # TODO: add try-catch and logging when raise exceptions
        try:
            response = self._send_api_request(**request_args)
        except (ConnectTimeout, ReadTimeout) as e:  # NOQA
            pass
        if response and response.status_code != HTTPStatus.OK:
            response = None
        self._response = response
        return response

    # which is easy to be mocked
    @staticmethod
    def _send_api_request(*args, **kwargs) -> Response:
        return requests.get(*args, **kwargs)

    @staticmethod
    def extract_data(response: Response) -> Optional[BaseModel]:
        if not response:
            return None

        data = json.loads(response.content.decode('utf-8'))
        return ScoreboardV3.model_validate(data)

    def get_data(self, overwritten: bool = False) -> Optional[BaseModel]:
        response = self._response
        if not self._response or overwritten:
            response = self.request()

        data_model = self.extract_data(response)
        return data_model
