from pathlib import Path
from custom_nodes.ComfyUI_NAIDGenerator.nodes import GenerateNAID
import folder_paths

class Mutix2_GenerateNAID(GenerateNAID):
    def __init__(self):
      super().__init__()

    def initialize(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        input_dict = super().INPUT_TYPES()

        input_dict["required"]["positive"] = ("STRING",  {"forceInput":True})
        input_dict["required"]["negative"] = ("STRING",  {"forceInput":True})
        input_dict["required"]["width"]    = ("INT", {"forceInput":True})
        input_dict["required"]["height"]   = ("INT", {"forceInput":True})

        input_dict["optional"]["sub_folder_path"]    = ("STRING",)
        input_dict["optional"]["smea_optional"]      = ("STRING", {"forceInput":True})
        input_dict["optional"]["sampler_optional"]   = ("STRING", {"forceInput":True})
        input_dict["optional"]["scheduler_optional"] = ("STRING", {"forceInput":True})

        return input_dict

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "00_kento_nodes"

    def generate(self, limit_opus_free, width, height, positive, negative, steps, cfg, decrisper, smea, sampler, scheduler, seed, uncond_scale, cfg_rescale, option=None, sub_folder_path="", smea_optional=None, sampler_optional=None, scheduler_optional=None):

      #改修1.optionalに入力があった場合書き換え
      smea      = smea_optional      if smea_optional else smea
      sampler   = sampler_optional   if sampler_optional else sampler
      scheduler = scheduler_optional if scheduler_optional else scheduler

      #改修2.sub_folder_pathのパスをoutput_dirに変更
      self.output_dir = folder_paths.get_output_directory()
      if sub_folder_path.strip():
        sub_folder = Path(self.output_dir) / sub_folder_path.strip()
        self.output_dir = str(sub_folder.resolve())

      result = super().generate(limit_opus_free, width, height, positive, negative, steps, cfg, decrisper, smea, sampler, scheduler, seed, uncond_scale, cfg_rescale, option)

      return result

def get_scale_size(width, height):
  if (width,height) == (832,1216):
    width,height = (1280,1856)
  elif (width,height) == (1216,832):
    width,height = (1856,1280)
  elif (width,height) == (1024,1024):
    width,height = (1536,1536)

  return (width, height)


class ImgScaleNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "switch"     : ("BOOLEAN", {"default":True}),
                "width"      : ("INT", {"forceInput":True}),
                "height"     : ("INT", {"forceInput":True}),
            },
        }

    RETURN_NAMES = ("width", "height",)
    RETURN_TYPES = ("INT", "INT",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, switch, width, height):
      if switch:
        return get_scale_size(width, height)
      else:
        return (width, height)


class Muti2x_Enhance_Switch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enhanced": ("BOOLEAN",{"default":False}),
                "option"     : ("NAID_OPTION",),
                "width"      : ("INT", {"forceInput":True}),
                "height"     : ("INT", {"forceInput":True}),
                "smea"       : ("STRING", {"forceInput":True}),
                "seed"       : ("INT", {"forceInput":True}),
            },
            "optional": {
                "new_seed"   : ("INT", {"forceInput":True}),
            }
        }

    RETURN_NAMES = ("option", "width", "height", "smea", "seed", "is_enhanced",)
    RETURN_TYPES = ("NAID_OPTION", "INT", "INT", "STRING", "INT","BOOLEAN")
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, is_enhanced, option, width, height, smea, seed, new_seed=None):
      print(option)
      if is_enhanced:
        (width, height) = get_scale_size(width, height)
        smea = "none"
      else:
        if "img2img" in option:
          del option["img2img"]

      #注意:ここはswitchの値に関わらずnew_seedに値が入ってくれば値が上書き
      seed = new_seed if new_seed else seed

      return (option, width, height, smea, seed, is_enhanced,)


NODE_CLASS_MAPPINGS = {
  "Mutix2_GenerateNAID":Mutix2_GenerateNAID,
  "ImgScaleNode":ImgScaleNode,
  "Muti2x_Enhance_Switch":Muti2x_Enhance_Switch,
}