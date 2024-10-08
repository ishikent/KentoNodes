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



NODE_CLASS_MAPPINGS = {
  "PromptFormatter":PromptFormatter,
  "Muti2x_TextBox":Muti2x_TextBox,
}