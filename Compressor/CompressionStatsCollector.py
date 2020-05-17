class CompressionStatsCollector(object):

	UNITS = ['B', 'KB', 'MB', 'GB', 'TB']

	def __init__(self):
		self._total_bytes_in = 0
		self._total_bytes_out = 0

	def add_image_data(self, bytes_before: int, bytes_after: int):
		self._total_bytes_in += bytes_before
		self._total_bytes_out += bytes_after

	def get_total_bytes_in(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._total_bytes_in)

	def get_total_bytes_out(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._total_bytes_out)

	def get_diff(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._total_bytes_in - self._total_bytes_out)

	def get_actual_compression_ratio_percentage(self) -> float:
		if self._total_bytes_in == 0:
			return 0
		else:
			return round(self._total_bytes_out / float(self._total_bytes_in) * 100, 2)

	@staticmethod
	def __convert_unit(input: int) -> str:
		unit_index = 0
		output = float(input)

		while output >= 1024:
			output = output / 1024.0
			unit_index += 1

		return str(round(output, 2)) + ' ' + CompressionStatsCollector.UNITS[unit_index]