from uuid import uuid4
import hashlib

from db import connection


def _get_password_hash(password):
	return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password, first_name='', last_name='', email=''):
	password_hash = _get_password_hash(password)
	with connection.cursor() as cursor:
		cursor.execute(
			"INSERT INTO users "
			"(username, password, first_name, last_name, email)"
			" VALUES (%s, %s, %s, %s, %s)",
			(username, password_hash, first_name, last_name, email)
		)

	connection.commit()


def check_password(user_id, password):
	password_hash = _get_password_hash(password)
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
		user = cursor.fetchone()

	return password_hash == user[2]


def authenticate_user(username, password):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
		user = cursor.fetchone()

	if check_password(user[0], password):
		return user


def create_user_session(user_id):
	session_id = str(uuid4())
	with connection.cursor() as cursor:
		cursor.execute(
			"INSERT INTO sessions (id, user_id) VALUES (%s, %s)",
			(session_id, user_id)
		)
		connection.commit()

	return session_id


def _get_session(cursor, session_id):
	cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
	return cursor.fetchone()


def _get_user(cursor, user_id):
	cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
	return cursor.fetchone()


def get_user_by_session_id(session_id):
	with connection.cursor() as cursor:
		session = _get_session(cursor, session_id)
		if not session: return
		user_id = session[1]
		user = _get_user(cursor, user_id)

	return user


def get_user_by_id(user_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
		user = cursor.fetchone()

	return user


def logout_user(user_id):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM sessions WHERE user_id = %s", (user_id,))
		session = cursor.fetchone()
		if session:
			cursor.execute(
				"DELETE FROM sessions WHERE user_id = %s", (user_id,)
			)

	connection.commit()


def get_all_posts():
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM posts")
		posts = cursor.fetchall()

	return posts


def create_post_for_user(title, short_description, text, author):
	with connection.cursor() as cursor:
		cursor.execute(
			"INSERT INTO posts (title, short_description, text, author)"
			"VALUES (%s, %s, %s, %s)", (title, short_description, text, author)
		)

	connection.commit()
