from .nodes import NODE_CLASS_MAPPINGS
import custom_nodes.KentoNodes.nai_nodes as nai_nodes
import custom_nodes.KentoNodes.data_dist_nodes as ddn
import custom_nodes.KentoNodes.text_nodes as text_nodes

NODE_CLASS_MAPPINGS.update(nai_nodes.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(ddn.NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(text_nodes.NODE_CLASS_MAPPINGS)

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS',"WEB_DIRECTORY"]
# __all__ = ['NODE_CLASS_MAPPINGS']

