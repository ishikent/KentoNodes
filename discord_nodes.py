import json
import requests

BOT_TOKEN = "MTI4NjUyMTU1MTQ0NDkwMTk0MA.Gc47Mm.IQcmMfQERR0ZGeV1ZIIPNIQuxJA6gkjJ6sj944"

#！！！！！！！これはチャンネル毎なので注意！！！！！！！！！！
WEBHOOK_URL = "https://discord.com/api/webhooks/1286514131985236010/ZcBiHZZzUkESyjMPE-ebCqNnSrmhXVk4hFlQwTE0MffqlaGbH4BSd8rjQPBgaFTCzRhQ"



def create_thread(thread_name):
  channel_id = "1286587501217054731"
  API_URL = f"https://discord.com/api/v10/channels/{channel_id}/threads"

  headers = {
      "Authorization" : f"Bot {BOT_TOKEN}",
      "Content-Type"  : "application/json",
  }

  data = {
      "name": f"{thread_name}",
      "auto_archive_duration":10080,
      "type" : 11, #公開スレッド
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
  print(response.status_code)


class Discord_Uploader:
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required":{
        "data_dir": ("STRING", {"default":"/home/kento/Downloads/upload"}),
      }
    }

  OUTPUT_NODE = True
  CATEGORY = "00_kento_nodes"
  FUNCTION = "run"

  def run(self, data_dir):
    create_thread(thread_name)
    return 


if __name__ == "__main__":
  thread_id = create_thread("New スレッド")
  print(thread_id)

  from pathlib import Path
  file_list = list(Path("images/").glob("*"))
  post_files(thread_id, file_list)
