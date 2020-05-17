import os

from CrawlerDto import CrawlerDto

class FileSystemUtils(object):

	IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.j2k', '.j2p', '.jpx', '.svg', '.bmp', '.gif', '.tiff', '.webp', '.eps']

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
