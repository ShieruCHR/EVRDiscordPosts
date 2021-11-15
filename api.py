import asyncio
import models
import aiohttp
import async_timeout
import json
from logging import getLogger

logger = getLogger(__name__)
async def empty(*args, **kwargs):
    pass

last_game_status = ""
on_game_status_change = empty
on_goal = empty
on_game_end = empty
on_round_end = empty
on_launch = empty

async def fetch(session: aiohttp.ClientSession, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            text = await response.text()
            return text

async def post_webhook(session: aiohttp.ClientSession, content: str, url):
    async with async_timeout.timeout(10):
        async with session.post(url, data={"content": content}) as response:
            text = await response.text()
            return text

async def run(host: str = "127.0.0.1", port: int = 6721, endpoint: str = "/session", interval: float = 1):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                data = await fetch(session, f"http://{host}:{port}{endpoint}")
                logger.debug(f"API Result: {data}")
                await parse(models.APIResult(json.loads(data)))
            except aiohttp.ClientConnectionError as e:
                logger.debug("Failed to call EchoVR API.", exc_info=e)
            except Exception as e:
                logger.warning("Failed to call EchoVR API.", exc_info=e)
            await asyncio.sleep(interval)

async def parse(data: models.APIResult):
    global last_game_status
    if last_game_status != data.game_status and data.game_status != models.GameStatus.UNKNOWN and data.game_status != models.GameStatus.EMPTY:
        await _game_status_change(last_game_status, data.game_status, data)
        last_game_status = data.game_status

async def _game_status_change(old: models.GameStatus, new: models.GameStatus, data: models.APIResult):
    logger.info(f"Game Status changed: {old} -> {new}")
    await on_game_status_change(data, old, new)
    if new == models.GameStatus.SCORE:
        await on_goal(data, data.last_score)
    if new == models.GameStatus.POST_MATCH:
        await on_game_end(data)
    if new == models.GameStatus.ROUND_OVER:
        await on_round_end(data)
    if new == models.GameStatus.PLAYING:
        await on_launch(data)