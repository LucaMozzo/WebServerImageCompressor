class CrawlerDto(object):

	def __init__(self):
		self.files = []

	def push(self, file: str):
		self.files.append(file)

	def pop(self) -> str or None:
		if len(self.files) > 0:
			element = self.files[-1]
			self.files.remove(element)
			return element
		return None

	def empty(self) -> bool:
		return len(self.files) == 0

	def get_files_count(self) -> int:
		return len(self.files)
