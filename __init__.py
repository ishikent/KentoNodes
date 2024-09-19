from .nodes import NODE_CLASS_MAPPINGS
from .nai_nodes import Mutix2_GenerateNAID

NODE_CLASS_MAPPINGS["Mutix2_GenerateNAID"] = Mutix2_GenerateNAID

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',"WEB_DIRECTORY"]
# __all__ = ['NODE_CLASS_MAPPINGS']

