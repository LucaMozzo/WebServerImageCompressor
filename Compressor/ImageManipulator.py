from PIL import Image


class ImageManipulator(object):

	@staticmethod
	def compress(file_path: str, output_path: str, quality: int):
		image = Image.open(file_path)
		image.save(output_path, optimize=True, quality=quality)
