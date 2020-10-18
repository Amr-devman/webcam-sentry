import os
import sqlite3
from sqlite3 import Error


#creates a new swlite db for the user
def create_connection(db_file):

	conn = None

	db_filepath = os.path.join("dbs", db_file)

	try:
		conn = sqlite3.connect(db_filepath)
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()


