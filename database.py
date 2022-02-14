import psycopg2.extras

import config

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)