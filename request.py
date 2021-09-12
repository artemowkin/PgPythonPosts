from urllib.parse import unquote_plus

from services import get_user_by_session_id


class HttpRequest:

	def __init__(self, environ):
		self._environ = environ

	@property
	def path(self):
		return self._environ['PATH_INFO']

	@property
	def cookies(self):
		if not 'HTTP_COOKIE' in self._environ:
			return {}

		cookies_list = self._environ['HTTP_COOKIE'].split('; ')
		cookies_dict = dict([cookie.split('=') for cookie in cookies_list])
		return cookies_dict

	@property
	def user(self):
		if hasattr(self, '_user'):
			return self._user
		elif not 'sessionkey' in self.cookies:
			self._user = None
		else:
			session_key = self.cookies.get('sessionkey')
			self._user = get_user_by_session_id(session_key)

		return self._user

	@property
	def method(self):
		return self._environ['REQUEST_METHOD']

	@property
	def data(self):
		if not hasattr(self, '_dict_data'):
			length = int(self._environ.get('CONTENT_LENGTH', '0'))
			string_data = self._environ['wsgi.input'].read(length).decode()
			string_data = unquote_plus(string_data)
			list_data = [element.split('=') for element in string_data.split('&')]
			self._dict_data = dict(list_data)

		return self._dict_data
