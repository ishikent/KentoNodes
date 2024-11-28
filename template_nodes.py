from pathlib import Path
import folder_paths
from PIL import Image,ImageOps
import json
from pathlib import Path
import os
import numpy as np
import torch

class Muti2x_SD_Reader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "root"         : ("STRING", {}),
                "dirname"      : ("STRING", {}),
                "index"        : ("INT", {}),
                # "file"       : ("STRING", {}),
            },
        }

    RETURN_NAMES = ("positives", "negatives", "images",)
    RETURN_TYPES = ("STRING", "STRING", "IMAGE",)
    FUNCTION = "run"
    CATEGORY = "00_kento_nodes"
    # OUTPUT_IS_LIST = (True, True,True,)

    def run(self, root, dirname, index):
      target_dir = Path(root) / dirname

      #画像取得
      images = self.load_images(target_dir.resolve())
      positives, negatives = self.load_prompts(target_dir)

      idx = index % len(images)
      return (positives[idx],negatives[idx],images[idx],)

    #サブ
    def load_prompts(self, directory: str):
      label = {}
      label["positive"] = "prompt"
      label["negative"] = "uc"
      positives = []
      negatives = []

      for file in sorted(directory.glob("*.png")):
        img = Image.open(file)

        data = json.loads(img.info["Comment"])
        positives.append(data.get(label["positive"] ,""))
        negatives.append(data.get(label["negative"] ,""))

      return (positives,negatives,)

    #サブ
    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")
        dir_files = os.listdir(directory)
        if len(dir_files) == 0:
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        # Filter files by extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]

        dir_files = sorted(dir_files)
        dir_files = [os.path.join(directory, x) for x in dir_files]

        # start at start_index
        dir_files = dir_files[start_index:]

        images = []

        limit_images = False
        if image_load_cap > 0:
            limit_images = True
        image_count = 0

        for image_path in dir_files:
            if os.path.isdir(image_path) and os.path.ex:
                continue
            if limit_images and image_count >= image_load_cap:
                break
            i = Image.open(image_path)
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            images.append(image)
            image_count += 1

        return images


NODE_CLASS_MAPPINGS = {
  "Muti2x_SD_Reader":Muti2x_SD_Reader,
}