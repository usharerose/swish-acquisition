"""
Celery tasks
"""
import datetime
import logging

from swish_acquisition.celery_app import app
from swish_acquisition.collectors import ScoreboardCollector


logger = logging.getLogger(__name__)


@app.task
def scrape_daily_scoreboard(game_date: str, league_id: str):
    a_date = datetime.datetime.strptime(game_date, '%Y-%m-%d').date()
    collector = ScoreboardCollector(game_date=a_date, league_id=league_id)
    collector.run()
