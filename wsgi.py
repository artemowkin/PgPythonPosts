from request import HttpRequest
from response import Http404Response


def get_response(request):
	from urls import urlpatterns
	view = urlpatterns.get(request.path)
	if not view:
		return Http404Response(
			"<h1>404 Not Found</h1><p>View for "
			f"path `{request.path}` doesn't exist</p>"
		)

	return view(request)


class WSGIApplication:

	def __init__(self, environ, start_response):
		self.environ = environ
		self.start_response = start_response

	def __iter__(self):
		request = HttpRequest(self.environ)
		response = get_response(request)
		self.start_response(str(response.status), response.headers)
		yield response.data


application = WSGIApplication
