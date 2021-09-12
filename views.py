from response import HttpResponse
from services import (
	authenticate_user, create_user_session, create_user, logout_user,
	get_all_posts, create_post_for_user, get_user_by_id
)


def homepage(request):
	return HttpResponse('<h1>Homepage</h1>')


def login(request):
	if request.method == 'GET':
		return HttpResponse(
			'<html><head><meta charset="utf-8"><title>Log In</title></head>'
			'<body><form method="POST">'
			'<p><label>Username: </label><input name="username" required></p>'
			'<p><label>Password: </label><input name="password" type="password" required></p>'
			'<p><button type="submit">Log In</button></p>'
			'</form></body></html>'
		)
	elif request.method == 'POST':
		if request.user:
			return HttpResponse('<h1>Already logged in</h1>')

		user = authenticate_user(**request.data)
		two_weeks_in_seconds = 2*7*24*60*60
		if user:
			session_key = create_user_session(user[0])
			return HttpResponse('<h1>Successfully logged in!</h1>', headers=[
				('Set-Cookie', (
					 f'sessionkey={session_key}; '
					 f'Max-Age={two_weeks_in_seconds}; Path=/')
				)
			])

		return HttpResponse(
			'<html><head><meta charset="utf-8"><title>Log In</title></head>'
			'<body><form method="POST">'
			'<h3>Data is incorrect</h3>'
			'<p><label>Username: </label><input name="username" required></p>'
			'<p><label>Password: </label><input name="password" type="password" required></p>'
			'<p><button type="submit">Log In</button></p>'
			'</form></body></html>'
		)


def logout(request):
	if request.method == 'GET':
		return HttpResponse(
			'<html><head><meta charset="utf-8"><title>Log Out</title></head>'
			'<body><form method="POST">'
			'<p><button type="submit">Log Out</button></p>'
			'</form></body></html>'
		)
	if request.method == 'POST':
		if not request.user:
			return HttpResponse("<h1>You're not logged in</h1>")

		logout_user(request.user[0])
		return HttpResponse('<h1>Successfully logged out</h1>', headers=[
			('Set-Cookie', (
				 'sessionkey=deleted; '
				 'expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/')
			)
		])


def signup(request):
	if request.method == 'GET':
		return HttpResponse(
			'<html><head><meta charset="utf-8"><title>Sign Up</title></head>'
			'<body><form method="POST">'
			'<p><label>Username: </label><input name="username" required></p>'
			'<p><label>Password: </label><input name="password1" type="password" required></p>'
			'<p><label>Password (twice): </label><input name="password2" type="password" required></p>'
			'<p><button type="submit">Sign Up</button></p>'
			'</form></body></html>'
		)
	elif request.method == 'POST':
		password1 = request.data['password1']
		password2 = request.data['password2']
		if not password1 == password2:
			return HttpResponse(
				'<html><head><meta charset="utf-8"><title>Sign Up</title></head>'
				'<body><form method="POST">'
				'<h3>Passwords are differently</h3>'
				'<p><label>Username: </label><input name="username" required></p>'
				'<p><label>Password: </label><input name="password1" type="password" required></p>'
				'<p><label>Password (twice): </label><input name="password2" type="password" required></p>'
				'<p><button type="submit">Sign Up</button></p>'
				'</form></body></html>'
			)

		create_user(request.data['username'], password1)
		return HttpResponse('<h1>Successfully signed up</h1>')


def posts(request):
	posts = get_all_posts()
	response_text = (
		'<html><head><meta charset="UTF-8"><title>Posts</title></head><body>'
	)
	for post_id, title, short_description, text, author, pub_date in posts:
		author = get_user_by_id(author)
		response_text += (
			f"<h2>{title}</h2><p>{short_description}</p>"
			f"<small><b>{author[1]}</b> ({pub_date})</small>"
		)

	response_text += "</body></html>"
	return HttpResponse(response_text)


def create_post(request):
	if request.method == 'GET':
		return HttpResponse(
			'<html><head><meta charset="UTF-8"><title>Create Post</title>'
			'</head><body><form method="POST">'
			'<p>Title: <input name="title" required></p>'
			'<p>Short Description: <input name="short_description" required></p>'
			'<p>Text: <textarea name="text" required></textarea></p>'
			'<p><button type="submit">Create</button></p>'
			'</form></body></html>'
		)
	if request.method == 'POST':
		post_data = request.data | {'author': request.user[0]}
		create_post_for_user(**post_data)
		return HttpResponse(
			'<html><head><meta charset="UTF-8"><title>Create Post</title>'
			'</head><body><h1>Successfully created!</h1></body></html>'
		)
