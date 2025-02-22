from .nodes import NODE_CLASS_MAPPINGS
import custom_nodes.KentoNodes.nai_nodes as nai_nodes
import custom_nodes.KentoNodes.data_dist_nodes as ddn
import custom_nodes.KentoNodes.text_nodes as text_nodes
import custom_nodes.KentoNodes.template_nodes as template_nodes
import custom_nodes.KentoNodes.remote_nodes as remote_nodes
import custom_nodes.KentoNodes.db_nodes as db_nodes
import server
from PIL import Image
from io import BytesIO

NODE_CLASS_MAPPINGS.update(nai_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(ddn.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(text_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(template_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(remote_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(db_nodes.NODE_CLASS_MAPPINGS)

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',"WEB_DIRECTORY"]
# __all__ = ['NODE_CLASS_MAPPINGS']

import logging

# 既存ルートが登録されているかどうかを確認する関数
def is_route_defined(route):
    for r in server.PromptServer.instance.routes:
        if r.path == route:
            return True
    return False

# ルートを一度だけ定義する関数
def add_route_once():
    route = "/kento/send_image"

    # すでにルートが定義されている場合は追加しない
    if not is_route_defined(route):
        @server.PromptServer.instance.routes.post(route)
        async def send_image(request):
            data = await request.post()
            image_file = data["image"]

            # 画像ファイルをバイナリとして読み込む
            image_bytes = await image_file.read()

            # PIL.Imageとして変換
            image = Image.open(BytesIO(image_bytes))

            # クライアントでテキストを更新するメッセージを送信
            server.PromptServer.instance.send_sync("send_imgage", data)

        logging.debug(f"Route {route} has been added.")
    else:
        logging.debug(f"Route {route} already exists, skipping definition.")

# ルートの定義は、例えばアプリケーションが初期化されるタイミングで呼ばれる
add_route_once()