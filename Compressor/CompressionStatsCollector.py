class CompressionStatsCollector(object):

	UNITS = ['B', 'KB', 'MB', 'GB', 'TB']

	def __init__(self):
		self._totalBytesIn = 0
		self._totalBytesOut = 0

	def add_image_data(self, bytes_before: int, bytes_after: int):
		self._totalBytesIn += bytes_before
		self._totalBytesOut += bytes_after

	def get_total_bytes_in(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._totalBytesIn)

	def get_total_bytes_out(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._totalBytesOut)

	def get_diff(self) -> str:
		return CompressionStatsCollector.__convert_unit(self._totalBytesOut - self._totalBytesIn)

	def get_actual_compression_ratio_percentage(self) -> float:
		return round(self._totalBytesIn / float(self._totalBytesOut) * 100, 2)

	@staticmethod
	def __convert_unit(input: int) -> str:
		unit_index = 0
		output = float(input)

		while output >= 1024:
			output = output / 1024.0
			unit_index += 1

		return str(round(output, 2)) + ' ' + CompressionStatsCollector.UNITS[unit_index]