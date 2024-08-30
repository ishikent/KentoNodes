from .imgutil import cv2pil,pil2cv,crop_and_resize
import numpy as np
import sys
from segment_anything import sam_model_registry, SamPredictor
from PIL import Image
import torch
from torchvision import transforms

class SAMDetector:

  def load_model(self):
    sam_checkpoint = "/home/kento/projects/ComfyUI/models/sam/sam_vit_h_4b8939.pth"
    model_type     = "vit_h"

    self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)

    device = "cuda"
    self.sam.to(device=device)

  def samMask2MaskImg(self, mask):
      # マスクの形状を取得
      h, w = mask.shape

      # マスクを白と黒の画像に変換
      # Trueは白 (255), Falseは黒 (0)に設定
      mask_image = np.zeros((h, w, 3), dtype=np.uint8)
      mask_image[mask == True] = [255, 255, 255]  # 白
      mask_image[mask == False] = [0, 0, 0]  # 黒

      return mask_image

  #PILを渡してPILで返す
  def get_sam_mask_PIL(self, image_pil,input_box):
    image_pil = image_pil.convert("RGB")
    image_cv = pil2cv(image_pil)

    predictor = SamPredictor(self.sam)
    predictor.set_image(image_cv) 

    masks, scores, logits = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=False,
    )

    mask_image = self.samMask2MaskImg(masks[0])
    print(f"score = {scores[0]}")
    img = Image.fromarray(mask_image)
    img = img.convert("L")
    return img

    #multimask_outputがTrueの場合
    # for i in range(len(masks)):
    #   mask_image = samMask2MaskImg(masks[i])

    #   img = Image.fromarray(mask_image)
    #   print(f"score = {scores[i]}")
    #   img.save(f"mask_{scores[i]}_.png")


if __name__ == "__main__":

  image_pil = Image.open("ero.png")

  x0, y0 = 101,982
  x1 , y1 = x0 + 185, y0 + 228
  input_box = np.array([x0, y0, x1, y1]) # [x0, y0, x1, y1]

  sam_detector = SAMDetector()
  sam_detector.load_model()

  img = sam_detector.get_sam_mask_PIL(image_pil, input_box)
  img.save("mskmsk.png")
