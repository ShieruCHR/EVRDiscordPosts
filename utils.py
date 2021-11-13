from datetime import timedelta
from models import MatchType, Team
import random

def get_team(teams: list[Team], player_name: str):
    for team in teams:
        for p in team.players:
            if p.player.name == player_name:
                return team
    return None

def timedelta_to_str(delta: timedelta):
    mm, ss = divmod(delta.seconds, 60)
    s = "%d分%02d秒" % (mm, ss)
    return s

print(timedelta_to_str(timedelta(minutes=5, seconds=30, microseconds=120)))