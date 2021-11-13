from models import MatchType, Team
import random

def get_team(teams: list[Team], player_name: str):
    for team in teams:
        for p in team.players:
            if p.player.name == player_name:
                return team
    return None

def generate_tweet_text(gamemode: MatchType, team, blue, orange, username):
    l = [
        "{gamemode}において、{team}として{blue}対{orange}で勝利しました！ - {username}".format(gamemode=gamemode.name.replace("_", " ").title(), team=team, blue=blue, orange=orange, username=username)
    ]
    return random.choice(l)