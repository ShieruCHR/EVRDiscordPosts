import asyncio
from discord_webhook.webhook import DiscordEmbed
import config
import datetime

from discord_webhook import DiscordWebhook

import api
from models import APIResult, GameStatus, GoalInfo
from utils import timedelta_to_str
from logging import WARNING, basicConfig, getLogger

basicConfig(level=WARNING)
logger = getLogger(__name__)
last_launch = None

async def change(data: APIResult, old: GameStatus, new: GameStatus):
    pass

async def goal(data: APIResult, goal_info: GoalInfo):
    webhook = DiscordWebhook(
        url=config.WEBHOOK_URL
    )
    embed = DiscordEmbed(title=f'ゴール！ - {goal_info.goal_type.name.replace("_", " ").title()}', description=f":{goal_info.team}_square: {goal_info.team.title()}チームに{goal_info.point_amount}ポイント！")
    embed.add_embed_field(name="シュートしたプレイヤー", value=goal_info.player_name, inline=False)
    if goal_info.assistted_player_name != "[INVALID]":
        embed.add_embed_field(name="Assisted By", value=goal_info.assistted_player_name, inline=False)
    embed.add_embed_field(name="シュート距離", value=f"{round(goal_info.distance_thrown, 2)}メートル")
    embed.add_embed_field(name="シュート速度", value=f"{round(goal_info.disc_speed, 2)}m/s")
    embed.add_embed_field(name="Launchからの経過時間", value=f"{timedelta_to_str(datetime.datetime.utcnow() - last_launch)}")
    
    webhook.add_embed(embed)
    webhook.execute()

async def launch(data: APIResult):
    global last_launch
    last_launch = datetime.datetime.utcnow()
    logger.info(f"Launch: {last_launch}")

async def over(data: APIResult):
    webhook = DiscordWebhook(
        url=config.WEBHOOK_URL
    )
    beat_team = data.teams[int(data.blue_round_score < data.orange_round_score)]
    embed = DiscordEmbed(title='Round Over!', description=f"ラウンド終了、このラウンドは{beat_team.name.title()}チームの勝利です！")
    embed.add_embed_field(name=f"スコア", value=f":orange_square: {data.orange_points} - {data.blue_points} :blue_square:")
    webhook.add_embed(embed)
    webhook.execute()

async def end(data: APIResult):
    webhook = DiscordWebhook(
        url=config.WEBHOOK_URL, 
        content=''
    )
    embed = DiscordEmbed(title='Game Ended!', description="ゲーム終了、お疲れさまでした！")
    embed.add_embed_field(name="マッチタイプ", value=data.match_type.name.replace("_", " ").title())
    embed.add_embed_field(name=f"ラウンド数 {data.total_round_count}回", value=f":orange_square:オレンジチーム ラウンド勝利数: {data.orange_round_score}\n:blue_square:ブルーチーム ラウンド勝利数: {data.blue_round_score}", inline=False)
    webhook.add_embed(embed)
    webhook.execute()

api.on_game_status_change = change
api.on_goal = goal
api.on_game_end = end
api.on_round_end = over
api.on_launch = launch

def main():
    logger.info(f"Configuration: Call http://{config.HOST}:{config.PORT}{config.ENDPOINT} per {config.INTERVAL} seconds.")
    logger.info(f"Discord Webhook URL: {config.WEBHOOK_URL}")
    loop = asyncio.get_event_loop()
    task = loop.create_task(api.run(host=config.HOST, port=config.PORT, endpoint=config.ENDPOINT, interval=config.INTERVAL))
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.critical("An internal error occurred, aborting.", exc_info=e)


if __name__ == '__main__':
    main()