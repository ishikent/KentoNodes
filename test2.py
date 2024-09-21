import requests
import json

# Webhook URLを設定
WEBHOOK_URL = 'https://discord.com/api/webhooks/1286514131985236010/ZcBiHZZzUkESyjMPE-ebCqNnSrmhXVk4hFlQwTE0MffqlaGbH4BSd8rjQPBgaFTCzRhQ'

# Discord APIトークン (ユーザーではなくBotが必要)
DISCORD_TOKEN = 'MTI4NjUyMTU1MTQ0NDkwMTk0MA.GW48zQ.7_NE_h5HJL9pJIFeq9hocn0Hd3dQewJapP2Ig8'

# 投稿する画像のパス
file_path = 'data/ero.png'

# 1. Webhookでメッセージを送信
with open(file_path, 'rb') as f:
    files = {
        'file': f
    }
    data = {
        'content': 'This message will be used to create a thread.'
    }
    response = requests.post(WEBHOOK_URL, data=data, files=files)

# 2. WebhookのメッセージIDを取得
if response.status_code == 200:
    message_id = response.json()['id']
    channel_id = response.json()['channel_id']
else:
    print(f"Failed to send message: {response.status_code}")
    exit()

# 3. メッセージを元にスレッドを作成
THREAD_API_URL = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/threads'

headers = {
    'Authorization': f'Bot {DISCORD_TOKEN}',  # Botトークンが必要です
    'Content-Type': 'application/json'
}

# スレッドの名前を指定
thread_data = {
    'name': 'New Thread from Webhook Message',
    'auto_archive_duration': 1440  # スレッドのアーカイブ時間（60は1時間）
}

# スレッド作成のリクエストを送信
thread_response = requests.post(THREAD_API_URL, headers=headers, data=json.dumps(thread_data))

if thread_response.status_code == 201:
    print("Thread created successfully!")
else:
    print(f"Failed to create thread: {thread_response.status_code}, {thread_response.text}")
