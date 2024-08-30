from nudenet import NudeDetector

"""

detect and detect_batch accept
file path(s), opencv image(s), image bytes(s), open(image_path, 'rb') (buffereader) objects

"""
class NudeNet_Utils:
	ROOT_PATH = "/home/kento/projects/ComfyUI/models/onnx"
	MODELS    = {"320":"320n.onnx", "640":"640m.onnx"}
	LABELS = [
						"FEMALE_GENITALIA_COVERED",
						"FACE_FEMALE",
						"BUTTOCKS_EXPOSED",
						"FEMALE_BREAST_EXPOSED",
						"FEMALE_GENITALIA_EXPOSED",
						"MALE_BREAST_EXPOSED",
						"ANUS_EXPOSED",
						"FEET_EXPOSED",
						"BELLY_COVERED",
						"FEET_COVERED",
						"ARMPITS_COVERED",
						"ARMPITS_EXPOSED",
						"FACE_MALE",
						"BELLY_EXPOSED",
						"MALE_GENITALIA_EXPOSED",
						"ANUS_COVERED",
						"FEMALE_BREAST_COVERED",
						"BUTTOCKS_COVERED"
  				]

	@classmethod
	def get_nudenet_result(cls, image, select_res):

		detector   = NudeDetector(model_path=f"{cls.ROOT_PATH}/{cls.MODELS[select_res]}", inference_resolution=int(select_res))
		result = detector.detect(image)

		return result

if __name__ == "__main__":

	select_res = "640"
	image_list = "nsfw.png"

	result = NudeNet_Utils.get_nudenet_result(image_list, select_res)
	print(result)