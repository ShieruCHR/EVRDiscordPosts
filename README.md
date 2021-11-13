# EchoVR Result Posting
EchoVRのゴール、ラウンド終了などの情報をWebhookを使ってDiscordサーバーに送りつけるプログラムです。  

# How to use
**Require: Python 3.5 or later**  

1. config.pyを編集して、DiscordのWebhook URLを指定します。
2. EchoVRの設定画面からAPIアクセスを許可し、EchoVRを再起動します。
3. `main.py`を実行します。
4. ほっとくだけでDiscordに情報が送りつけられます。

# Note
はじめて非同期処理を書いた上にコードレビューとかしてもらったことないんでスパゲッティもいいとこです。  
その上バグバグしてたり不安定だったりするかもしれません、何かあったらIssue立てて教えて下さい。

Python 3.9.7, PCでのみテストしています。configの`HOST`をいじればQuestでも動くかもしれませんが、非推奨です。  

現状一人ぼっちのPrivate Matchでのみテストしていますが理論上はPublicでも動くはずです。  
一緒にテストしてくれる優しい方がいれば、https://discord.gg/4JpMy2k8 に来て声かけてください。

AI TeammatesはAPIから情報が来なかったんでサポートしていません。