# DiscordのWebhook URL
WEBHOOK_URL = "https://example.com"

# EchoVR APIのIPアドレス。基本的にはデフォルトで問題ありません。
HOST = "127.0.0.1"

# EchoVR APIのポート番号。基本的にはデフォルトで問題ありません。
PORT = 6721

# EchoVR APIのエンドポイント。基本的にはデフォルトで問題ありません。
ENDPOINT = "/session"

# EchoVR APIを呼んでから、次に呼ぶまでの待ち時間。秒単位で指定します。
# この値を長くすると送信が遅れたり、そもそも送られなかったりします。
#
# 基本的には1秒で問題ありませんが、不具合が生じたりある程度の精度が要求される場合はこの値を下げてください。
INTERVAL = 1

