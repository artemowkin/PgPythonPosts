import psycopg2
from psycopg2.errors import DuplicateTable

import settings


connection = psycopg2.connect(**settings.DATABASE)


def _create_users_table():
	with connection.cursor() as cursor:
		sql = ("CREATE TABLE users ("
			"id SERIAL NOT NULL PRIMARY KEY,"
			"username VARCHAR(256) UNIQUE NOT NULL,"
			"password VARCHAR(256) NOT NULL,"
			"first_name VARCHAR(125) NOT NULL,"
			"last_name VARCHAR(125) NOT NULL,"
			"email VARCHAR(256) NOT NULL"
			");"
		)
		cursor.execute(sql)


def _create_posts_table():
	with connection.cursor() as cursor:
		sql = ("CREATE TABLE posts ("
			"id SERIAL NOT NULL PRIMARY KEY,"
			"title VARCHAR(256) NOT NULL,"
			"short_description VARCHAR(256) NOT NULL,"
			"text TEXT NOT NULL,"
			"author INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,"
			"pub_date DATE NOT NULL DEFAULT current_date"
			");"
		)
		cursor.execute(sql)


def _create_sessions_table():
	with connection.cursor() as cursor:
		sql = ("CREATE TABLE sessions ("
			"id UUID NOT NULL PRIMARY KEY,"
			"user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE"
			");"
		)
		cursor.execute(sql)


def create_db():
	_create_users_table()
	_create_posts_table()
	_create_sessions_table()
	connection.commit()
