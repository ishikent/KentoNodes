from .nodes import NODE_CLASS_MAPPINGS
import custom_nodes.KentoNodes.nai_nodes as nai_nodes
import custom_nodes.KentoNodes.data_dist_nodes as ddn
import custom_nodes.KentoNodes.text_nodes as text_nodes
import custom_nodes.KentoNodes.template_nodes as template_nodes
import custom_nodes.KentoNodes.remote_nodes as remote_nodes
import aiohttp
import server

NODE_CLASS_MAPPINGS.update(nai_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(ddn.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(text_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(template_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(remote_nodes.NODE_CLASS_MAPPINGS)

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',"WEB_DIRECTORY"]
# __all__ = ['NODE_CLASS_MAPPINGS']

@server.PromptServer.instance.routes.post("/send_image")
async def send_image(request):
    data = await request.json()

    port = 8188 #これマジックナンバーで指定してるので、後で変更する
    async with aiohttp.ClientSession() as session:
        #Comfyサーバーに画像を送信
        async with session.post(f"localhost:{port}/upload/image", data=data) as response:
            return aiohttp.web.Response(status=response.status)

    #recieve_imageノードに情報を送信
    overwrite = data.get("overwrite", False)
    subfolder = data.get("subfolder", "")
    type = data.get("type", "")

    img_info = {
        "overwrite": overwrite,
        "subfolder": subfolder,
        "type": type
    }
    # クライアントでテキストを更新するメッセージを送信
    server.PromptServer.instance.send_sync("send_imgage", data)