"""
Celery tasks
"""
import datetime
import logging
import time

from swish_acquisition.celery_app import app
from swish_acquisition.collectors import (
    BoxscoreSummaryCollector,
    CommonPlayerInfoCollector,
    PlayByPlayCollector,
    ScoreboardCollector,
    TeamDetailsCollector
)


logger = logging.getLogger(__name__)


@app.task
def scrape_daily_scoreboard(game_date: str, league_id: str):
    a_date = datetime.datetime.strptime(game_date, '%Y-%m-%d').date()
    collector = ScoreboardCollector(game_date=a_date, league_id=league_id)
    collector.run()


@app.task
def scrape_single_game_series(game_date: str, game_id: str):
    a_date = datetime.datetime.strptime(game_date, '%Y-%m-%d').date()

    # 01. collect Boxscore Summary
    boxscore_summary = BoxscoreSummaryCollector(game_date=a_date, game_id=game_id)
    boxscore_summary.run()

    # 02. collect Team Details of game's both sides
    for _, team_id in boxscore_summary.get_team_ids().items():
        if not team_id:
            continue
        team_details = TeamDetailsCollector(game_date=a_date, team_id=team_id)
        team_details.run()
        time.sleep(3)

    # 03. collect Common Player Info of game's related players
    for _, player_ids in boxscore_summary.get_player_ids().items():
        if not player_ids:
            continue
        for player_id in player_ids:
            common_player_info = CommonPlayerInfoCollector(game_date=a_date, player_id=player_id)
            common_player_info.run()
            time.sleep(3)

    # 04. collect Play By Play
    play_by_play = PlayByPlayCollector(game_date=a_date, game_id=game_id)
    play_by_play.run()
