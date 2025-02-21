class ImageReciever:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE", {}),
            }}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"

    def run(self, image):
        return (image,)


NODE_CLASS_MAPPINGS = {
    "ImageReciever": ImageReciever
}
