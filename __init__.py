from .nodes import NODE_CLASS_MAPPINGS
from .nai_nodes import Mutix2_GenerateNAID,Muti2x_Enhance_Switch
import custom_nodes.KentoNodes.data_dist_nodes as ddn
import custom_nodes.KentoNodes.text_nodes as text_nodes

NODE_CLASS_MAPPINGS["Mutix2_GenerateNAID"] = Mutix2_GenerateNAID
NODE_CLASS_MAPPINGS["Muti2x_Enhance_Switch"] = Muti2x_Enhance_Switch

NODE_CLASS_MAPPINGS.update(ddn.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(text_nodes.NODE_CLASS_MAPPINGS)

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',"WEB_DIRECTORY"]
# __all__ = ['NODE_CLASS_MAPPINGS']

