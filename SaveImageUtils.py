from PIL import Image
from PIL.PngImagePlugin import PngInfo


#メタデータをJsonで取得する（pythonでは辞書）
def get_new_pnginfo(old_image):
  pnginfo = old_image.text

  new_pnginfo = PngInfo()

  for key, value in pnginfo.items():
    new_pnginfo.add_text(key, "114514")

  return new_pnginfo
  # old_image.save(filename, pnginfo=new_pnginfo)

#ComfyUIでロードした画像には普通メタデータが無いため、NAIのメタデータの構造は固定で入れておく
def get_new_pnginfo_kotei():
  nai_json = '{"Title":"114514","Description":"114514","Software":"114514","Source":"114514","Generation time":"114514","Comment":"114514"}'
  pnginfo = json.loads(nai_json)

  new_pnginfo = PngInfo()
  for key, value in pnginfo.items():
    new_pnginfo.add_text(key, value)

  return new_pnginfo
  

def get_image_alpha255(old_image):
  new_image = old_image.convert("RGB")
  # new_image.putalpha(255)
  return new_image

import json
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pygments import highlight

def read_pnginfo(image):
  metadata  = image.text
  dump_data = json.dumps(metadata, indent=4, separators=("\n", ":"))
  print(highlight(dump_data, JsonLexer(), TerminalFormatter()))


if __name__ == "__main__":

  new_path = "/home/kento/Downloads/new.png"

  #画像用見込み
  old_image = Image.open("test.png")


  #上書き用メタデータ取得
  pnginfo = get_new_pnginfo(old_image)

  
  #非透過アルファチャネルを持つimageオブジェクトを取得
  new_image = get_image_alpha255(old_image)

  #保存
  new_image.save(new_path, pnginfo = pnginfo)

  #新規画像のメタデータを確認
  test_image = Image.open(new_path)
  read_pnginfo(test_image)
