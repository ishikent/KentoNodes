from custom_nodes.KentoNodes.node_utils import text_utils

class PromptFormatter:
  @classmethod
  def INPUT_TYPES(s):
        return {
            "required": {
                "prompt" : ("STRING", {"forceInput":True}),
            },
        }
  RETURN_NAMES = ("prompt",)
  RETURN_TYPES = ("STRING",)
  FUNCTION = "run"
  CATEGORY = "00_kento_nodes"

  def run(self, prompt):
    formatted_prompt = text_utils.get_formatted_prompt(prompt)
    return (formatted_prompt,)


class Muti2x_TextBox(PromptFormatter):
  @classmethod
  def INPUT_TYPES(s):
        input_dict = super().INPUT_TYPES()
        input_dict["required"]["prompt"] = ("STRING", {"multiline":True})

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
                "prompt" : ("STRING", {"forceInput":True}),
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
              "prefix" : ("STRING", {}),
              "prompt" : ("STRING", {}),
              "suffix" : ("STRING", {}),
            },
        }

  RETURN_NAMES = ("prompt",)
  RETURN_TYPES = ("STRING",)
  FUNCTION = "run"
  CATEGORY = "00_kento_nodes"

  def run(self, prefix, prompt, suffix):
    new_prompt = f"{prefix},{prompt},{suffix}"
    return (new_prompt,)


NODE_CLASS_MAPPINGS = {
  "PromptFormatter":PromptFormatter,
  "Muti2x_TextBox":Muti2x_TextBox,
  "Muti2x_Pony_Positive":Muti2x_Pony_Positive,
  "Muti2x_Pony_Negative":Muti2x_Pony_Negative,
  "Muti2x_PreSuffix":Muti2x_PreSuffix,
}