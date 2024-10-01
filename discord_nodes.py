import json
import requests

BOT_TOKEN = "MTI4NjUyMTU1MTQ0NDkwMTk0MA.Gp9z8A.kDJlEKtSP-7ojMmV0WEeRaO5F10h9KjIizkEBg"

#！！！！！！！これはチャンネル毎なので注意！！！！！！！！！！
#basic
WEBHOOK_URL = "https://discord.com/api/webhooks/1287275012621078681/62uJ6SLjIizRcSsl4srkda7AEYrvEcRkV7QS6W-kV5vEUa6dqTWV6fAGleoTrkxnh_fp"

#スケジュールﾁｬﾝﾈﾙ
WEBHOOK_URL_2 = "https://discord.com/api/webhooks/1287407386293698663/JBMYTKkjz7k7Ogc5isWOwRB37N6V3Vf3dgBZLt3QkUUgHWCfDBvrBnFzyI2Spg66H10I"


def create_thread(thread_name):
  channel_id = "1287316741948575798"
  API_URL = f"https://discord.com/api/v10/channels/{channel_id}/threads"

  headers = {
      "Authorization" : f"Bot {BOT_TOKEN}",
      "Content-Type"  : "application/json",
  }

  data = {
      "name": f"{thread_name}",
      "auto_archive_duration":10080,
      "type" : 11, # 11:公開スレッド, 12:非公開スレッド
  }

  response = requests.post(API_URL, headers=headers, json=data)


  if response.status_code == 201:
      print("thread created!!")
      return response.json()["id"]
  else:
      print(f"{response.status_code}:{response.text}")
      return None

import more_itertools
def post_files(thread_id, file_path_list):
   for i, chunked in enumerate(more_itertools.chunked(file_path_list, 10)):
      print(f"分割{i}回目のリクエスト")
      post_files_limited(thread_id, chunked)

def post_files_limited(thread_id, file_path_list):

  #下記の形式
  # files = {
  #   "files[0]": open("data/ero.png",  "rb"),
  #   "files[1]": open("data/ero2.jpg", "rb"),
  # }
  files = {f"files[{i}]":open(file_path, "rb") for i, file_path in enumerate(file_path_list)}

  #discord側で画像の順番を保ったまま表示して欲しいのでattachmentを使う
  #"attachments":[
  #   {"id":0},
  #   {"id":1},
  #],
  attachment = [{"id":i} for i in range(len(file_path_list))]

  payload = {
     "username"   : "muti2x_bot",
     "avatar_url" : "https://cdn.discordapp.com/attachments/1286662186160099428/1286662353794105354/WithoutMeta_00002_.png?ex=66eeb932&is=66ed67b2&hm=6f464182d294be1346a452ef6d7e37502545f7d438366b727a7066467cf3052d&",
     "attachment" : attachment
  }
  
  WITH_THREAD = f"{WEBHOOK_URL}?thread_id={thread_id}"
  response = requests.post(WITH_THREAD, files=files, data={"payload_json":json.dumps(payload)})
  print(f"{response.status_code} - {response.text}")

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
def get_publish_date(args):

    zoneinfo = ZoneInfo("Asia/Tokyo")

    # 現在の日時を取得
    now = datetime.now(zoneinfo)

    # 年と月が指定されていない場合は、現在の年と月を使用
    year = args.year if args.year else now.year
    month = args.month if args.month else now.month

    # フォーマットされたISO8601形式の日付を返す
    return f"{year}-{month:02d}-{args.day:02d}T{args.hour:02d}:{args.minute:02d}"

# 関数を直接実行して結果を確認する場合はコメントアウトを外す
# print(post_schedule())


def post_schdule_message(URL, thread_id, publish_date, debug=False):
  # data = {
  #   "content":f"thread_id@{thread_id},publish_date@2024-09-22T22:55"
  # }
  data = {
    "content":f"thread_id@{thread_id},publish_date@{publish_date}"
  }

  if debug:
    print(data)
    return data
  
  #debug=Falseの場合のみ実行
  requests.post(URL, data=data)

def get_now_date():
  return datetime.now().strftime("%Y-%m-%dT%H:%M")

def post_schdule_message_debug(URL, thread_id, publish_date):
  post_schdule_message(URL, thread_id, publish_date, debug=True)


def initialize_args():
  # argparseの設定
  parser = argparse.ArgumentParser(description="Schedule a post with optional year and month.")

  # # 必須引数: 日、時、分
  # parser.add_argument("day", type=int, help="Day of the month")
  # parser.add_argument("hour", type=int, help="Hour of the day (0-23)")
  # parser.add_argument("minute", type=int, help="Minute of the hour (0-59)")

  # # オプション引数: 年、月（デフォルトは現在の日時から）
  # parser.add_argument("--year", type=int, help="Year (default is the current year)")
  # parser.add_argument("--month", type=int, help="Month (default is the current month)")

  parser.add_argument("name", type=str, help="Minute of the hour (0-59)")

  # 引数の解析
  return parser.parse_args()


if __name__ == "__main__":
  """
  Webhook urlと紐づくチャンネルに対して、ファイルの自動投稿を行う

  1.create_threadメソッドで引数に指定した名前で新規スレッドを作成
  例.2024/10/01_一ノ瀬アスナ

  2.post_filesメソッドで上の新規スレッドにファイルを投稿
  ※discordのファイル投稿の上限は10個までなので、それ以上の数がある場合は自動で分割投稿する

  """

  args = initialize_args()

  thread_id = create_thread(args.name)
  print(thread_id)

  from pathlib import Path
  file_list = list(Path("images/").glob("*"))
  file_list.sort()
  post_files(thread_id, file_list)
  
  file_list = list(Path("zip_and_pdf/").glob("*"))
  post_files(thread_id, file_list)


  """予約投稿機能はスレッドの公開・非公開の切り替えが難しい
  ためにメンションを使ってやってたが、それも難しいのでちょっと保留

  """
  URL = f"{WEBHOOK_URL_2}"

  # publish_date = get_publish_date(args) #これは予約投稿用のメソッド、
  publish_date = get_now_date()
  post_schdule_message(URL, thread_id, publish_date)

