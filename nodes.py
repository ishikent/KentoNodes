class Counter:
    def __init__(self):
        self.count = 0

    def current(self):
        return self.count

    def count_up(self):
        self.count = self.count + 1

    def initialize(self):
        self.count = 0

class KentoStrInput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"multiline": True}),
            "seed": ("INT:seed", {})
            }}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        self.counter = Counter()

    def run(self, text, seed = None):
        text = f"{{{text}}} = {self.counter.count_up()}"
        return (text,)

# from enum import Enum

# class Mode(Enum):
#     COUNTUP = "count_up"
#     FIXED = "fixed"
#     RESET = "reset"
    

class ChainFileReader:
    @classmethod
    def INPUT_TYPES(s):
        return {
                    "required": {
                        "root_path": ("STRING", {"default":"/home/kento/Downloads/text_dir/prompt"}),
                        "file_path": ("STRING", {"forceInput" : False, "multiline": False}),
                        "seed"     : ("INT:seed", {}),
                    },
                    "optional": {
                        "previous_chain" : ("ANY", {"default":""}),
                    },
                }

    RETURN_TYPES = ("ANY", "STRING",)
    RETURN_NAMES = ("next_chain", "end_string",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, root_path, file_path, seed, previous_chain=[]):
        with open(f"{root_path}/{file_path}".strip(), "r") as f:
            self.lines = [line.strip() for line in f if not line.strip().startswith('#')]

        output_list = previous_chain + self.lines

        result = ""
        if output_list:
            result = ",".join(output_list)


        return (output_list, result,)

#注意メソッド
def getWordsFromTexts(text):
    return [word.strip() for word in text.split(",")]


def load_file(root_path,name):
    with open(f"{root_path}/{name}".strip(), "r") as f:
        lines = [line.strip() for line in f if ((line.strip()) and (not line.strip().startswith('#')))]

    return lines


def text_write(text):
    words = getWordsFromTexts(text)
    with open(f"{root_path}/{file_path}", "a") as f:
        f.write(",".join(words) + "\n")


import re
from collections import defaultdict
class Muti2xPromptEditor:
    @classmethod
    def INPUT_TYPES(s):
        return {
                    "required": {
                        "text": ("STRING", {"multiline":True}),
                        "seed"     : ("INT:seed", {}),
                    },
                }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def parse(self, text):
        words = getWordsFromTexts(text)

        dd = defaultdict(list)

        for word in words:
            if result := re.search(r"\((.*)\)", word):
                dd["loader"].append(result.group(1))
            
        return dd

    def load(self, name):
        root_path = "/home/kento/Downloads/text_dir/prompt/0_group"
        with open(f"{root_path}/{name}".strip(), "r") as f:
            lines = [line.strip() for line in f if ((line.strip()) and (not line.strip().startswith('#')))]

        if name =="quality":
            print(lines)

        result = ""
        if lines:
            result = ",".join(lines)

        return result


    def run(self, text, seed):
        dd = self.parse(text)

        replace_dict = {}

        for key in dd.keys():
            for name in dd[key]:
                file_text = self.load(name)

                if key == "loader":
                    replace_dict[f"({name})"] = file_text


        words = getWordsFromTexts(text)

        if len(words) == 0:
            return ("", )

        for replace_word in replace_dict.keys():
            print(replace_word)
            text = text.replace(replace_word, replace_dict[replace_word])
        # for i in range(len(words)):
        #     if replace_dict in words[i]:
        #         words[i] = words[i].replace() replace_dict[words[i]]

        # result = ",".join(words)

        return (text,)


class TextReplace:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "source_text" : ("STRING", {}),
                "insert_text" : ("STRING", {}),
                "replace_symbol" : ("STRING", {}),
            }
        }

    OUTPUT_NODE  = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, source_text, insert_text, replace_symbol):
        
        text = source_text.replace(replace_symbol, insert_text)

        return (text,)


import itertools
class WordPermutator:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "source_text" : ("STRING", {}),
                "perm_symbol" : ("STRING", {"default":"|"}),
            }
        }

    OUTPUT_IS_LIST = (True, )
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_list",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, source_text, perm_symbol):
        
        match = re.findall(f"\|(.*?)\|", source_text)

        #見つからなければテキストをそのまま返す
        if len(match) == 0:
            return ([source_text],)

        #最初にperm_symbolで囲まれた部分のみ順列をつくる。それ以降は無視
        first_range =  match[0]

        #範囲をリスト化  "one, two, three" = > ["one", "two", "three"]
        perm_list = first_range.split(",")


        replace_text = f"{perm_symbol}{first_range}{perm_symbol}" #後でテキストの該当箇所をreplaceするのに使う


        #順列リストの作成
        perm_result = [source_text.replace(replace_text ,",".join(perm)) for perm in itertools.permutations(perm_list)] #文字列のリストになる

        return (perm_result, )

class Debug:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "perm_output1" : ("STRING", {}),
            }
        }

    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = ()
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, perm_output1):
        print("==========DEBUG=================")
        for i, hoge in enumerate(perm_output1):
            print(f"=================OUTPUT{i}=====================")
            print(hoge)

        return ()   



class PermutateProduct:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "perm_output1" : ("STRING", {}),
                "perm_output2" : ("STRING", {}),
                "debug" : ("BOOLEAN", {"default":False}),
            }
        }

    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, )
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_list",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, perm_output1, perm_output2, debug):
        result = list(itertools.chain(perm_output1, perm_output2))

        if debug:
            for ele in result:
                print("==========================================")
                print(ele)

        return (result, )


class CounterFileReader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "text_path": ("STRING", {"forceInput" : False, "multiline": False}),
                    "mode": (["count_up","fixed","reset",], {}),
                },
                "optional": {
                    "seed": ("INT:seed", {}),
                }
                }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("line_text", "current_count",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        self.initialize_counter()

    def initialize_counter(self):
        self.counter = Counter()
        self.lines = None
        self.previous_text_path = ""

    def run(self, text_path, mode, seed):
        print(f"mode ======= {mode}")
        print(self.previous_text_path)
        if self.previous_text_path != text_path:
            print("initialize!!!")
            #Counterインスタンスを新しく作る
            self.initialize_counter()


        if (self.lines is not None) and (mode == "count_up"):
            print("count up")
            self.counter.count_up()

        if mode == "reset":
            print("count reset!!!")
            #Counterインスタンスは使い回し、カウンタ変数のみリセット
            self.counter.initialize()

        if self.lines is None:
            with open(text_path.strip(), "r") as f:
                self.lines = [line for line in f if not line.strip().startswith('#')]

        line = self.lines[self.counter.current() % len(self.lines)]

        self.previous_text_path = text_path

        return (line, str(self.counter.current()), )

class EasyFileWriter:
    MODE_APPEND    = "append"
    MODE_OVERWRITE = "overwrite"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "root_path" : ("STRING", {"default":"/home/kento/Downloads/text_dir/prompt/0_group"}),
                "file_path" : ("STRING", {}),
                "file_path" : ("STRING", {}),
                "text" : ("STRING", {"multiline":True}),
                "mode" : ([EasyFileWriter.MODE_APPEND, EasyFileWriter.MODE_OVERWRITE], {}),
            }
        }

    OUTPUT_NODE  = True
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, root_path, file_path, text, mode):

        mode_arg = "a" if mode == EasyFileWriter.MODE_APPEND else "w"

        words = getWordsFromTexts(text)
        with open(f"{root_path}/{file_path}", mode_arg) as f:
            f.write("\n".join(words) + "\n")


        return ()


import folder_paths
from .SaveImageUtils import get_image_alpha255, get_new_pnginfo_kotei
from PIL import Image, ImageDraw
import os
import numpy as np

class SaveImageWithCustomInfo:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "WithoutMeta", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."})
            },
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True
    CATEGORY = "00_kento_nodes"


    def save_images(self, images, filename_prefix="WithoutMeta"):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            #アルファチャネルを削除したImageオブジェクトを返す
            new_img = get_image_alpha255(img)

            metadata = get_new_pnginfo_kotei()

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            new_img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            counter += 1

        return ()


# class TextOutput:
#     @classmethod
#     def INPUT_TYPES(s):
#         return {"required": {"text": ("STRING", {"forceInput": True})}}
#     OUTPUT_NODE = True
#     RETURN_TYPES = ()
#     FUNCTION  = "run"
#     CATEGORY = "00_kento_nodes"

#     def run(self, text):
#         print(text)
#         return ()

class TextOutput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    RETURN_TYPES = ("STRING",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self):
        return ("Hello World", )


from .nsfw import NudeNet_Utils
from .imgutil import convertTensor2Np, convertNp2Tensor
from .imgutil import convertTensor2PIL, convertPIL2Tensor
import json
class NudeNetDetector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image"         : ("IMAGE", {}),
                "model_key"      : (list(NudeNet_Utils.MODELS.keys()), {}),
                "label"          : (NudeNet_Utils.LABELS, {}),
                "score_thres"    : ("FLOAT", {"default":0.3, "min":0, "max":1.0, "step":0.05,}),
            }
        }
    
    RETURN_TYPES   = ("ANY", "STRING", "STRING", "IMAGE", )
    RETURN_NAMES   = ("nude_bbox", "show_all_bbox","show_output_bbox", "image",)
    # OUTPUT_IS_LIST = (True, False, False,False,)

    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"
    # INPUT_IS_LIST = (True, False, False, False, False,)

    def run(self, image, model_key, label, score_thres=30.0):

        """
        detection_example = [
                                {'class': 'BELLY_EXPOSED', 'score': 0.799403190612793 , 'box': [64, 182, 49, 51]},
                                {'class': 'FACE_FEMALE'  , 'score': 0.7881264686584473, 'box': [82, 66, 36, 43]},
                            ]
        """

        # #map処理用の内部関数
        # #nudeinfo_listは1枚当たりの検出ボックス情報
        def is_ok(element):
            if element["class"] != label:
                return False
            
            if element["score"] < score_thres:
                return False

            return True

        image_tensor = image.clone().detach().cpu()
        image_np  = convertTensor2Np(image_tensor)
        result    = NudeNet_Utils.get_nudenet_result(image_np, model_key)
        tmp = list(filter(is_ok, result))

        # #保存テスト
        # pil_img = Image.fromarray(image_np)
        # pil_img.save("/home/kento/projects/ComfyUI/custom_nodes/KentoNodes/ttt.png")

        output_img = convertNp2Tensor(image_np)

        nude_bbox = tmp[0] if len(tmp) else {}

        return (nude_bbox, json.dumps(result, indent=4), json.dumps(nude_bbox, indent=4), output_img,)

import torch
class NudeNetBBox:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image"     : ("IMAGE", {}),
            "nude_bbox" : ("ANY", {}),
        }}

    RETURN_TYPES = ("IMAGE", "MASK",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, image, nude_bbox):
        #マスク画像を新規作成
        image_size = convertTensor2PIL(image).size # (1216, 832)
        print(image_size)
        mask_pil = Image.new("L", image_size, 0)

        #矩形書き込み
        bbox_x, bbox_y, bbox_w, bbox_h = nude_bbox["box"]
        draw = ImageDraw.Draw(mask_pil)

        bbox = (bbox_x, bbox_y, bbox_x + bbox_h, bbox_y + bbox_h)
        draw.rectangle(bbox, fill="white")


        #ComfyUIでは[1, 1216, 832]という風に3軸にする必要があるのでunsqueezeする
        nude_mask = convertPIL2Tensor(mask_pil)

        # print(nude_mask.shape)

        return (image,nude_mask, )

from .sam import SAMDetector
class NudeNetSAM:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image"     : ("IMAGE", {}),
            "nude_bbox" : ("ANY", {}),
        }}

    RETURN_TYPES = ("IMAGE", "MASK",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        #最初だけ実行
        #Segment Anythingロード
        self.sam_detector = SAMDetector()
        self.sam_detector.load_model()

    def run(self, image, nude_bbox):
        image_pil = convertTensor2PIL(image)

        #バウンディングボックス
        if nude_bbox:
            bbox_x, bbox_y, bbox_w, bbox_h = nude_bbox["box"]
            x0, y0, x1, y1 = (bbox_x, bbox_y, bbox_x + bbox_h, bbox_y + bbox_h)
            input_box = np.array([x0, y0, x1, y1]) # [x0, y0, x1, y1]

            #SAMでマスク取得
            sam_mask_pil = self.sam_detector.get_sam_mask_PIL(image_pil, input_box)
            # sam_mask_pil.save("mskmsk.png")

        else:
            #事前処理でbboxが空だった場合は新規のマスクを返す
            image_size = convertTensor2PIL(image).size # (1216, 832)
            sam_mask_pil = Image.new("L", image_size, 0)


        nude_sam_mask = convertPIL2Tensor(sam_mask_pil)

        return (image, nude_sam_mask, )

import json
class PresetWriter:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "file_pointer" : ("ANY", {}),
            "label" : ("STRING", {}),
            "text"  : ("STRING", {"multiline":True,}),
            "mode":(["nothing","add,replace","remove","clear"], {}),
        }}

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, file_pointer, label, text, mode):

        #何もしない
        if mode == "nothing":
            return ()

        #全部消す
        if mode == "clear":
            print(mode)
            file_pointer.write("")
            return ()

        #jsonファイル読込
        preset_json = file_pointer.load()
        preset_json =  preset_json if preset_json else "{}"
        preset = json.loads(preset_json)

        #テキスト正則化
        words = getWordsFromTexts(text)

        if mode == "remove":
            del preset[label]
        else:
            #辞書にセット
            preset[label] = ",".join(words)

        #ファイル書き込み
        file_pointer.write(json.dumps(preset, ensure_ascii=False))

        return ()


class PresetReader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "file_pointer" : ("ANY", {}),
            "label" : ("STRING", {}),
        }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"


    def run(self, file_pointer, label):
        text = file_pointer.load()
        preset = json.loads(text)

        if label in preset:
            result = preset[label]
        else:
            result = ""
        
        return (result,)



import codecs
class FilePointer:
    def __init__(self, filename):
        self.filename = filename
    
    def load(self):
        with codecs.open(self.filename, "r","utf-8") as f:
            text = f.read()
        
        return text

    def write(self, text):
        with codecs.open(self.filename, "w", "utf-8") as f:
            f.write(text)

    def getFilePath(self):
        return self.filename

    def getLines(self):
        with codecs.open(self.filename, "r","utf-8") as f:
            lines = [line.replace("\n","").strip() for line in f if not line.strip().startswith('#')]
        
        return lines


class TextWoList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "pre_text_list" : ("ANY", {}),
                "text_a" : ("STRING", {"forceInput": True}),
                "text_b" : ("STRING", {"forceInput": True}),
                "text_c" : ("STRING", {"forceInput": True}),
                "text_d" : ("STRING", {"forceInput": True}),
                "text_e" : ("STRING", {"forceInput": True}),
                "text_f" : ("STRING", {"forceInput": True}),
                "text_g" : ("STRING", {"forceInput": True}),
        }}

    RETURN_TYPES = ("STRING","ANY",)
    RETURN_NAMES = ("text_list","text_list_chain",)
    OUTPUT_IS_LIST = (True,False,)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self,**text_list):
        print()
        print()
        print("===========================================")
        print(text_list)

        if "pre_text_list" in text_list:
            result = list(itertools.chain(text_list.pop("pre_text_list"), text_list.values()))
        else:
            result = list(text_list.values())

        print("=---------result")
        print(result)

        return (result, result, )

class PresetCyclicReader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "file_pointer": ("ANY", {}),
                    "mode": (["count_up","fixed","reset",], {}),
                },
                "optional": {
                    "seed": ("INT:seed", {}),
                }
                }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("label", "value",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def __init__(self):
        self.initialize_counter()

    def initialize_counter(self):
        self.counter = Counter()
        self.keys = None
        self.values = None
        self.previous_text_path = ""

    def run(self, file_pointer, mode, seed):
        print(f"mode ======= {mode}")
        print(self.previous_text_path)
        if self.previous_text_path != file_pointer.getFilePath():
            print("initialize!!!")
            #Counterインスタンスを新しく作る
            self.initialize_counter()


        if (self.keys is not None) and (mode == "count_up"):
            print("count up")
            self.counter.count_up()

        if mode == "reset":
            print("count reset!!!")
            #Counterインスタンスは使い回し、カウンタ変数のみリセット
            self.counter.initialize()

        if self.keys is None:
                lines = file_pointer.getLines()
                text  = "".join(lines)
                text_json = json.loads(text)
                self.keys   = list(text_json.keys())
                self.values = list(text_json.values())

        key   = self.keys[self.counter.current() % len(self.keys)]
        value = self.values[self.counter.current() % len(self.keys)]

        self.previous_text_path = file_pointer.getFilePath()

        return (key,value, )


class FilePointerProvider:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "root_path" : ("STRING", {}),
            "file_path" : ("STRING", {}),
            "mode" : (["r","w","a", "r+", "w+"], {"default":"w+"}),
        }}

    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("file_pointer",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, root_path, file_path, mode):
        first_path  = root_path.strip()
        second_path = file_path.strip()

        fp = FilePointer(f"{first_path}/{second_path}")
        return (fp, )


class NAI_Parser:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "settings" : ("STRING", {"forceInput": True}),
        }}

    RETURN_TYPES = ("STRING","STRING","STRING","FLOAT","FLOAT",)
    RETURN_NAMES = ("smea","sampler","scheduler","uncond_scale","cfg_rescale",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, settings):
        # 正規表現でキーと値をパースする
        pattern = r'(\w+): ([^,]+)(?:,|$)'
        matches = re.findall(pattern, settings)

        # 辞書に変換
        settings_dict = {key: value.strip() for key, value in matches}

        #smea
        sm     = settings_dict["sm"]
        sm_dyn = settings_dict["sm_dyn"]
        smea = "none"
        if sm_dyn == "True":
            smea = "SMEA+DYN"
        elif sm == "True":
            smea = "SMEA"

        #uncond_scale
        uncond_scale = float(settings_dict["uncond_scale"])

        #cfg_rescale
        cfg_rescale = float(settings_dict["cfg_rescale"])


        return (smea, settings_dict["sampler"], settings_dict["noise_schedule"],uncond_scale, cfg_rescale,)


class NAI_Params:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive" : ("STRING", {"forceInput": True}),
                "negative" : ("STRING", {"forceInput": True}),
                "settings" : ("STRING", {"forceInput": True}),
        }}

    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("nai_params",)
    FUNCTION  = "run"
    CATEGORY = "00_kento_nodes"

    def getSMEA(self, settings_dict):
        #smea
        sm     = settings_dict["sm"]
        sm_dyn = settings_dict["sm_dyn"]
        smea = "none"
        if sm_dyn == "True":
            smea = "SMEA+DYN"
        elif sm == "True":
            smea = "SMEA"
        
        return smea


    def run(self, positive, negative, settings):
        # 正規表現でキーと値をパースする
        pattern = r'(\w+): ([^,]+)(?:,|$)'
        matches = re.findall(pattern, settings)

        # 辞書に変換
        settings_dict = {key: value.strip() for key, value in matches}


        #nai_paramsを作る
        nai_params = {
            "positive"          : positive,
            "negative"          : negative,
            "seed"              : int(settings_dict["seed"]),
            "steps"             : int(settings_dict["steps"]),
            "cfg"               : float(settings_dict["scale"]),
            "width"             : int(settings_dict["width"]),
            "height"            : int(settings_dict["height"]),
            "smea"              : self.getSMEA(settings_dict),
            "sampler"           : settings_dict["sampler"],
            "scheduler"         : settings_dict["noise_schedule"],
            "uncond_scale"      : float(settings_dict["uncond_scale"]),
            "cfg_rescale"       : float(settings_dict["cfg_rescale"]),
        }

        return (nai_params,)


class NAI_Params_Parser:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "nai_params" : ("ANY", {}),
            }
        }

    RETURN_NAMES    = ("smea", "sampler", "scheduler", "width", "height", "positive", "negative", "steps", "cfg", "seed", "uncond_scale", "cfg_rescale",)
    RETURN_TYPES    = ("STRING", "STRING", "STRING", "INT", "INT", "STRING", "STRING", "INT", "FLOAT", "INT", "FLOAT", "FLOAT")
    FUNCTION        = "run"
    CATEGORY        = "00_kento_nodes"

    def run(self, nai_params):

        return [nai_params[key] for key in NAI_Params_Parser.RETURN_NAMES]

class muti2x_bool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "switch":("BOOLEAN", {"default":False}),
            }
        }

    RETURN_NAMES = ("boolean",)
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, switch):
        return (switch,)


class Muti2x_PDF_Convert:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name":("STRING", {}),
                "images":("IMAGE", {}),
            }
        }

    RETURN_NAMES = ()
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    INPUT_IS_LIST = True
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, name, images):
        # 画像を開き、RGBモードに変換してリストに格納
        image_list = [convertTensor2PIL(image).convert('RGB') for image in images]

        # 最初の画像を基にPDFを作成し、残りの画像を追加
        full_output_folder, _, _, _, _  = folder_paths.get_save_image_path("", folder_paths.get_output_directory(), images[0].shape[1], images[0].shape[0])
        save_path = os.path.join(full_output_folder, f"{name[0]}.pdf")
        print(save_path)
        image_list[0].save(save_path, save_all=True, append_images=image_list[1:])

        return ()



NODE_CLASS_MAPPINGS = {
    "KentoStrInput": KentoStrInput,
    "TextOutput": TextOutput,
    "CounterFileReader": CounterFileReader,
    "SaveImageWithCustomInfo": SaveImageWithCustomInfo,
    "NudeNetDetector": NudeNetDetector,
    "NudeNetBBox": NudeNetBBox,
    "NudeNetSAM": NudeNetSAM,
    "ChainFileReader": ChainFileReader,
    "EasyFileWriter": EasyFileWriter,
    "Muti2xPromptEditor": Muti2xPromptEditor,
    "TextReplace": TextReplace,
    "WordPermutator": WordPermutator,
    "PermutateProduct": PermutateProduct,
    "Debug": Debug,
    "FilePointerProvider": FilePointerProvider,
    "PresetWriter": PresetWriter,
    "PresetReader": PresetReader,
    "PresetCyclicReader": PresetCyclicReader,
    "TextWoList": TextWoList,
    "NAI_Parser": NAI_Parser,
    "NAI_Params": NAI_Params,
    "NAI_Params_Parser": NAI_Params_Parser,
    "muti2x_bool": muti2x_bool,
    "Muti2x_PDF_Convert": Muti2x_PDF_Convert,
}

