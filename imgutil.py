from torchvision.transforms import ToPILImage, ToTensor
import numpy as np
import cv2
from PIL import Image

def convertTensor2Np(tensor):
	return np.array(convertTensor2PIL(tensor))


def convertTensor2PIL(tensor_img):
	#バッチの軸を削除
	tensor = tensor_img[0]

	# テンソルの形状を確認
	if tensor.dim() == 3 and tensor.shape[-1] == 3:
		# テンソルの形状を (高さ, 幅, チャンネル数) から (チャンネル数, 高さ, 幅) に変換
		tensor = tensor.permute(2, 0, 1)

	# ToPILImageを使用してテンソルからPIL画像へ変換
	return ToPILImage()(tensor)

def convertPIL2Tensor(img_pil):
	return convertNp2Tensor(np.array(img_pil))

def convertNp2Tensor(img_np):

	if img_np.ndim == 3:
		#[C, H, W] => [H, W, C]に変換
		img_np = np.transpose(img_np, (1, 2, 0))

	img_tensor = ToTensor()(img_np).unsqueeze(0)

	return img_tensor



def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def crop_and_resize(image_pil, input_box, output_size=(1024, 1024)):
    image_pil = image_pil.convert("RGB")
    original_width, original_height = image_pil.size

    # バウンディングボックスの座標
    x0, y0, x1, y1 = input_box
    
    # クロップサイズを計算
    crop_width = x1 - x0
    crop_height = y1 - y0
    crop_center_x = (x0 + x1) // 2
    crop_center_y = (y0 + y1) // 2
    
    # 新しい画像サイズの設定
    new_width, new_height = output_size
    
    if original_width > new_width or original_height > new_height:
        # クロップサイズを設定（1024x1024または元の画像サイズ）
        crop_size = max(crop_width, crop_height, new_width, new_height)
        
        # クロップ範囲の計算
        crop_x0 = max(crop_center_x - crop_size // 2, 0)
        crop_y0 = max(crop_center_y - crop_size // 2, 0)
        crop_x1 = min(crop_x0 + crop_size, original_width)
        crop_y1 = min(crop_y0 + crop_size, original_height)
        
        # 画像をクロップ
        image_pil = image_pil.crop((crop_x0, crop_y0, crop_x1, crop_y1))
    
    # 画像をリサイズ
    resized_image = image_pil.resize(output_size, Image.LANCZOS)
    
    return resized_image