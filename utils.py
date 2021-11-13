from models import MatchType, Team
import random

def get_team(teams: list[Team], player_name: str):
    for team in teams:
        for p in team.players:
            if p.player.name == player_name:
                return team
    return None
