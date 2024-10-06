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


class SaveWithJPEGFormat:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "JPGFORMAT"})
            },
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True
    CATEGORY = "00_kento_nodes"


    def save_images(self, images, filename_prefix="WithoutMeta"):
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            #アルファチャネルを削除したImageオブジェクトを返す
            new_img = get_image_alpha255(img)

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.jpg"
            new_img.save(os.path.join(full_output_folder, file), "JPEG", quality=85)
            counter += 1

        return ()


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
  "SaveImageWithCustomInfo":SaveImageWithCustomInfo,
  "SaveWithJPEGFormat":SaveWithJPEGFormat,
  "Muti2x_PDF_Convert":Muti2x_PDF_Convert,
}