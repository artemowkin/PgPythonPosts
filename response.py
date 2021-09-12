class BaseResponse:

	def __init__(self, text, status=None, headers=None):
		self._text = text
		self._status = status or self.get_default_status()
		if headers:
			self._headers = self.get_default_headers() + headers
		else:
			self._headers = self.get_default_headers()

	@property
	def text(self):
		return self._text

	@property
	def data(self):
		return self._text.encode()

	@property
	def status(self):
		return self._status

	@property
	def headers(self):
		return self._headers

	def get_default_status(self):
		raise NotImplementedError

	def get_default_headers(self):
		return [('Content-Type', 'text/html')]


class HttpResponse(BaseResponse):

	def get_default_status(self):
		return 200


class Http404Response(BaseResponse):

	def get_default_status(self):
		return 404
