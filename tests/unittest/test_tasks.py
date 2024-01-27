"""
Celery tasks unittest cases
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from swish_acquisition.celery_app import app
from swish_acquisition.tasks import scrape_daily_scoreboard
from tests.utils import get_mocked_response


with open('tests/data/endpoints/scoreboardv3/2022-05-29.json', 'r') as fp:
    SCOREBOARD_V3_DATA = json.load(fp)


class TasksTestCases(TestCase):

    def setUp(self) -> None:
        self.origin_task_always_eager = app.conf.task_always_eager
        app.conf.task_always_eager = True

    def tearDown(self) -> None:
        app.conf.task_always_eager = self.origin_task_always_eager

    @patch('swish_acquisition.scoreboardv3.ScoreboardV3Endpoint._send_api_request')
    def test_scrape_daily_scoreboard(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(SCOREBOARD_V3_DATA).encode('utf-8')
        )
        scrape_daily_scoreboard(game_date='2022-05-29', league_id='00')
