from enum import Enum

class APIResult:
    def __init__(self, data: dict):
        # TODO: この辺の処理をちゃんとやる
        self.disc = data.get("disc", {})
        self.session_id = data.get("sessionid", "")
        self.game_clock_display = data.get("game_clock_display", "")
        self.game_status = GameStatus(data.get("game_status", "unknown"))
        self.session_ip = data.get("sessionip", "")
        self.match_type = MatchType(data.get("match_type", "unknown"))
        self.map_name = data.get("map_name", "")
        self.teams = [Team(team_data) for team_data in data.get("teams", [])]
        self.is_private = data.get("private_match", False)
        self.total_round_count = data.get("total_round_count", 0)
        self.blue_round_score = data.get("blue_round_score", 0)
        self.orange_round_score = data.get("orange_round_score", 0)
        self.blue_points = data.get("blue_points", 0)
        self.orange_points = data.get("orange_points", 0)
        self.client_name = data.get("client_name", "")
        self.last_score = GoalInfo(data.get("last_score", {}))

class Team:
    def __init__(self, data: dict) -> None:
        self.name = data.get("team", "INVALID TEAM")
        self.players = [TeamPlayer(player_data, self) for player_data in data.get("players", [])]
        self.possession = data.get("possession", False)
        self.stats = Stats(data.get("stats", {}))

class TeamPlayer:
    def __init__(self, data: dict, team):
        self.player = Player(data)
        self.team = team

class Player:
    def __init__(self, data: dict):
        self.name = data.get("name", "[INVALID]")
        self.stats = Stats(data.get("stats", {}))
        self.number = data.get("number", -1)
        self.level = data.get("level", -1)
        self.ping = data.get("ping", -1)

class Stats:
    def __init__(self, data: dict) -> None:
        self.possession_time = data.get("posession_time", 0)
        self.points = data.get("points", 0)
        self.saves = data.get("saves", 0)
        self.goals = data.get("goals", 0)
        self.stuns = data.get("stuns", 0)
        self.passes = data.get("passes", 0)
        self.catches = data.get("catches", 0)
        self.steals = data.get("steals", 0)
        self.blocks = data.get("blocks", 0)
        self.interceptions = data.get("interceptions", 0)
        self.assists = data.get("assists", 0)
        self.shots_taken = data.get("shots_taken", 0)

class GoalInfo:
    def __init__(self, data: dict) -> None:
        self.disc_speed = data.get("disc_speed", 0.0)
        self.team = data.get("team", "")
        self.goal_type = GoalType(data.get("goal_type", "UNKNOWN"))
        self.point_amount = data.get("point_amount", 0)
        self.distance_thrown = data.get("distance_thrown", 0.0)
        self.player_name = data.get("person_scored", "")
        self.assistted_player_name = data.get("assist_scored", "")

class GameStatus(Enum):
    # TODO: EMPTYをなんとかする
    EMPTY = ""
    PRE_MATCH = "pre_match"
    ROUND_START = "round_start"
    PLAYING = "playing"
    SCORE = "score"
    ROUND_OVER = "round_over"
    POST_MATCH = "post_match"
    PRE_SUDDEN_DEATH = "pre_sudden_death"
    SUDDEN_DEATH = "sudden_death"
    POST_SUDDEN_DEATH = "post_sudden_death"
    UNKNOWN = "unknown"

class MatchType(Enum):
    ECHO_ARENA = "Echo_Arena"
    ECHO_ARENA_PRIVATE = "Echo_Arena_Private"
    ECHO_COMBAT = "Echo_Combat"
    ECHO_COMBAT_PRIVATE = "Echo_Combat_Private"
    SOCIAL_2_0 = "Social_2.0"
    INVALID_GAMETYPE = "INVALID GAMETYPE"       # APIはInvalid GameTypeを返すことがある。
    UNKNOWN = "unknown"               # INVALID_GAMETYPEとは違い、未知のゲームタイプを表す。

class GoalType(Enum):
    # "[NO GOAL]", "SLAM DUNK", "INSIDE SHOT", "LONG SHOT", "BOUNCE SHOT", "LONG BOUNCE SHOT", "BUMPER_SHOT"
    NO_GOAL = "[NO GOAL]"
    SLAM_DUNK = "SLAM DUNK"
    INSIDE_SHOT = "INSIDE SHOT"
    LONG_SHOT = "LONG SHOT"
    BOUNCE_SHOT = "BOUNCE SHOT"
    LONG_BOUNCE_SHOT = "LONG BOUNCE SHOT"
    BUMPER_SHOT = "BUMPER SHOT"
    SELF_GOAL = "SELF GOAL"
    UNKNOWN = "UNKNOWN"
