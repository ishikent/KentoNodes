from custom_nodes.KentoNodes.node_utils import text_utils
import pathlib
from custom_nodes.KentoNodes.general import path_utils
import re


class Muti2x_Prompt_Escaper:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": ("STRING", {"forceInput": True}),
                "symbol": ("STRING", {"default": "|"}),  # default symbol is "|"
            },
        }

    RETURN_NAMES = ("dest",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, source, symbol="|"):
        """入力テキストの特殊文字 (){} をエスケープし、指定された記号を()に置き換える関数."""

        # 1. symbolで囲まれた部分を一意のプレースホルダーに置き換え
        placeholders = []

        def replace_symbol(match):
            placeholder = f"__symbol_placeholder_{len(placeholders)}__"
            placeholders.append(match.group(1))  # symbolで囲まれた内容を記録
            return placeholder

        # symbolで囲まれた部分をプレースホルダーに置き換え
        temp_source = re.sub(rf"\{symbol}(.+?)\{symbol}", replace_symbol, source)

        # 2. (){} をエスケープ
        temp_source = re.sub(r"([\(\)\{\}])", r"\\\1", temp_source)

        # 3. プレースホルダーを対応する(実は)の形式に戻す
        for idx, placeholder in enumerate(placeholders):
            temp_source = temp_source.replace(
                f"__symbol_placeholder_{idx}__", f"({placeholder})"
            )

        return (temp_source,)


class Muti2x_Prompt_Excluder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": ("STRING", {"forceInput": True}),
                "prompt": ("STRING", {"multiline": True}),
            },
        }

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, source, prompt):
        excl = set(text_utils.get_formatted_tokens(prompt))
        source_list = text_utils.get_formatted_tokens(source)
        result = ",".join([x for x in source_list if x not in excl])
        return (result,)


class Muti2x_PromptFormatter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, prompt):
        formatted_prompt = text_utils.get_formatted_prompt(prompt)
        return (formatted_prompt,)


class Muti2x_PromptSpacer(Muti2x_PromptFormatter):
    @classmethod
    def INPUT_TYPES(s):
        return super().INPUT_TYPES()

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, prompt):
        space_prompt = " ".join(super().run(prompt)[0].split("_"))
        return (space_prompt,)


class Muti2x_TextBox(Muti2x_PromptFormatter):
    @classmethod
    def INPUT_TYPES(s):
        input_dict = super().INPUT_TYPES()
        input_dict["required"]["prompt"] = ("STRING", {"multiline": True})

        return input_dict

    RETURN_NAMES = ("formatted_prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, prompt):
        formatted_prompt = text_utils.get_formatted_prompt(prompt)
        return (formatted_prompt,)


class Muti2x_Pony_Positive:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, prompt):
        new_prompt = f"score_9,score_8_up,score_7_up,score_6_up,score_5_up,score_4_up,{prompt},source_anime,rating_explicit"
        return (new_prompt,)


class Muti2x_Pony_Negative:
    @classmethod
    def INPUT_TYPES(s):
        return {}

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self):
        new_prompt = """
    source_furry,source_cartoon,
    monochrome, realistic, rough sketch, fewer digits, extra digits,
    western_artist,disney,marvel,overwatch,league_of_legends,the_simpsons,realistic,
    aca,ces,gpo
    """

        return (new_prompt,)


class Muti2x_PreSuffix:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prefix": ("STRING", {}),
                "prompt": ("STRING", {}),
                "suffix": ("STRING", {}),
            },
        }

    RETURN_NAMES = ("prompt",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, prefix, prompt, suffix):
        new_prompt = f"{prefix},{prompt},{suffix}"
        return (new_prompt,)


class Muti2x_Modifier:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "file_name": ("STRING", {}),
                "initialize": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "signed_hash": ("STRING", {"forceInput": True}),
                "seed": ("INT:seed", {}),
            },
        }

    RETURN_NAMES = ("text",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        self.previous_signed_hash = ""  # 画像変更の検知用

    def prompt2lines(self, prompt):
        return "\n".join([word.strip().replace(" ", "_") for word in prompt.split(",")])

    def lines2prompt(self, lines):
        return ",".join([word.replace(" ", "_") for word in lines.split()])

    def run(self, text, file_name, initialize, signed_hash="", seed=None):
        dirPath = pathlib.Path(f"{path_utils.get_root_path()}/text_dir/prompt/2_tmp/")
        filePath = dirPath / file_name
        file_text = ""

        # ディレクトリが存在しない場合作る
        if not dirPath.exists():
            dirPath.mkdir()

        # ファイルが存在しない、もしくは読込画像が変わった
        # なら初期化処理として書き込む
        conditions = [
            not filePath.exists(),
            signed_hash != self.previous_signed_hash,
            initialize,
        ]

        if any(conditions):
            text_utils.write_token_on_file(filePath.resolve(), text)

        ##----以下はファイルが存在する場合

        # ファイルの内容を反映する
        output_text = text_utils.get_formatted_prompt_from_file(filePath.resolve())
        self.previous_signed_hash = signed_hash

        return (output_text,)


NODE_CLASS_MAPPINGS = {
    "Muti2x_Prompt_Excluder": Muti2x_Prompt_Excluder,
    "Muti2x_PromptFormatter": Muti2x_PromptFormatter,
    "Muti2x_PromptSpacer": Muti2x_PromptSpacer,
    "Muti2x_TextBox": Muti2x_TextBox,
    "Muti2x_Pony_Positive": Muti2x_Pony_Positive,
    "Muti2x_Pony_Negative": Muti2x_Pony_Negative,
    "Muti2x_PreSuffix": Muti2x_PreSuffix,
    "Muti2x_Modifier": Muti2x_Modifier,
    "Muti2x_Prompt_Escaper": Muti2x_Prompt_Escaper,
}
