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
