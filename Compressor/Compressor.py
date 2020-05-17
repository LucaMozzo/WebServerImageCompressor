import time
from concurrent.futures import ThreadPoolExecutor

from Compressor.CompressionStatsCollector import CompressionStatsCollector
from Compressor.FileSystemUtils import FileSystemUtils
from Compressor.ImageManipulator import ImageManipulator
from console_progressbar import ProgressBar


class Compressor(object):

	def __init__(self, base_path_in: str, base_path_out: str, quality: int, log_path: str = None):
		self.failures = []
		self.base_path_in = base_path_in
		self.base_path_out = base_path_out
		self.quality = quality
		self.stats_collector = CompressionStatsCollector()
		self.image_manipulator = ImageManipulator(self.stats_collector)
		self.log_path = log_path

	def compress(self, max_threads: int = 10):
		crawler_result = FileSystemUtils.crawl(self.base_path_in)

		# set up progress bar
		self.progress = 0
		total = crawler_result.get_files_count()
		self.progress_bar = ProgressBar(total=total, prefix='0%', decimals=1, length=50, fill='▍', zfill='∙')
		self.progress_bar.print_progress_bar(0)

		process_started = round(time.time() * 1000)  # current time in ms

		pool = ThreadPoolExecutor(max_workers=max_threads)
		futures = pool.map(self.__perform_compression, crawler_result.files)

		for future in futures:
			if future is not None:
				future.wait()

		if len(self.failures) > 0 and self.log_path is not None:
			f = open(self.log_path, 'w')
			for failure in self.failures:
				f.write(failure + '\n')
			f.close()

		time_taken_s = round((time.time() * 1000 - process_started) / 1000.0, 3)

		print('\n{no_files} processed in {total_time}s with {failures} failures'.format(
			no_files=crawler_result.get_files_count(), total_time=time_taken_s, failures=len(self.failures)))
		print('\nBefore: {size_before}\nAfter: {size_after}\nSaved: {saved}\nCompression: {compression}%'.format(
			size_before=self.stats_collector.get_total_bytes_in(),
			size_after=self.stats_collector.get_total_bytes_out(), saved=self.stats_collector.get_diff(),
			compression=self.stats_collector.get_actual_compression_ratio_percentage()))

	def __perform_compression(self, file: str):
		try:
			output_file = FileSystemUtils.get_output_path(file, self.base_path_in, self.base_path_out)
			self.image_manipulator.compress(file, output_file, self.quality)
		except Exception as e:
			self.failures.append(file + ' - ' + str(e))
		finally:
			self.progress += 1
			self.progress_bar.print_progress_bar(self.progress)