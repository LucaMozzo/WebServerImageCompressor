import os

from Compressor.CrawlerDto import CrawlerDto


class FileSystemUtils(object):
	IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.j2k', '.j2p', '.jpx', '.svg', '.bmp', '.gif', '.tiff', '.webp',
						'.eps']

	@staticmethod
	def is_folder(path: str) -> bool:
		return os.path.isdir(path)

	@staticmethod
	def crawl(path: str) -> CrawlerDto:
		result = CrawlerDto()

		for root, dirs, files in os.walk('path', topdown=False, followlinks=False):
			for file in files:
				file_name, file_extension = os.path.splitext(file)
				if file_extension.lower() in FileSystemUtils.IMAGE_EXTENSIONS:
					result.push(file)

		return result

	@staticmethod
	def get_output_path(file_in: str, input_base_path: str, output_base_path: str) -> str:
		"""
		Get the output path of an image and create the directories
		:param file_in: The path to the uncompressed image
		:param input_base_path: The base path specified by the user
		:param output_base_path: The output path specified by the user
		:return: The new full path of the image
		"""
		new_img_path = file_in.replace(input_base_path, output_base_path)
		file_name, file_path = FileSystemUtils._split_file_name(new_img_path)
		os.makedirs(file_path)
		return new_img_path

	@staticmethod
	def _split_file_name(file_path: str) -> (str, str):
		"""
		Split file name and rest of the path
		:param file_path: The full path to the file
		:return: A tuple (full path, file name + ext)
		"""
		split_index = file_path.rindex(os.sep)
		return file_path[:split_index], file_path[split_index + 1:]