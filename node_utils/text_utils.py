from pathlib import Path

def get_formatted_tokens(prompt_or_file_text):
  """
  1.prompt_or_fileは区切り文字は改行コードorカンマで混在しているなのでまず改行コードで区切り、それをカンマでjoinすることで一種類に統一
  2.それをカンマで区切る。結果はトークンのリスト
  3.それをリスト内方表記で1つずつ処理。左右の空白をstripし、replaceでスペースをアンダーバーに変える
  """
  return [token.strip().replace(" ","_") for token in ",".join(prompt_or_file_text.split("\n")).split(",") if token and not token.startswith("#")]

def load_token_from_file(file_name):
  fpath = Path(file_name)
  with fpath.open(mode="r") as f:
    file_text = f.read()
    return get_formatted_tokens(file_text)


def write_token_on_file(file_name, prompt):
  fpath = Path(file_name)
  with fpath.open(mode="w") as f:
    f.write(prompt2lines(prompt))


def get_formatted_prompt(prompt):
  return ",".join(get_formatted_tokens(prompt))

def get_formatted_prompt_from_file(file_name):
  return ",".join(load_token_from_file(file_name))

def prompt2lines(prompt):
    return "\n".join(get_formatted_tokens(prompt))