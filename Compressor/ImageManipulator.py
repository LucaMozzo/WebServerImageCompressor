from PIL import Image
import os

from Compressor.CompressionStatsCollector import CompressionStatsCollector
from Compressor.FileSystemUtils import FileSystemUtils


class ImageManipulator(object):

	def __init__(self, stats_collector: CompressionStatsCollector):
		self.stats_collector = stats_collector

	def compress(self, file_path: str, output_path: str, quality: int):
		image = Image.open(file_path)

		# prevent PNGs saved as JPEG with Alpha profile to be saved as RGBA
		if image.mode == 'RGBA':
			file_name = FileSystemUtils.split_file_name(file_path)[1]
			if file_name[file_name.rindex('.'):].lower() == '.jpg' or file_name[file_name.rindex('.'):].lower() == '.jpeg':
				image = image.convert('RGB')

		image.save(output_path, optimize=True, quality=quality)
		self.stats_collector.add_image_data(os.path.getsize(file_path), os.path.getsize(output_path))
