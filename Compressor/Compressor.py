from concurrent.futures import ThreadPoolExecutor
import time
from Compressor.CrawlerDto import CrawlerDto
from Compressor.FileSystemUtils import FileSystemUtils
from Compressor.ImageManipulator import ImageManipulator


class Compressor(object):

	def __init__(self, quality):
		self.failures = []
		self.quality = quality

	def compress(self, crawler_result: CrawlerDto, max_threads: int = 10):
		self.crawler_result = crawler_result

		process_started = round(time.time() * 1000)  # current time in ms

		with ThreadPoolExecutor(max_workers=max_threads) as executor:
			while not self.crawler_result.empty():
				future = executor.submit(self.__perform_compression, self.crawler_result.pop())
				print(future.result())

		time_taken_s = round((time.time() * 1000 - process_started) / 1000.0, 3)
		print('Process ended in ' + str(time_taken_s) + 's')

	def __perform_compression(self, file: str):
		try:
			output_file = FileSystemUtils.get_output_path(file)
			ImageManipulator.compress(file, output_file, self.quality)
			return True
		except:
			return False

