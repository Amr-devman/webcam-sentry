from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
import os
import random
import string

from db_functions import create_connection, create_creds_and_whitelist_tables
app = Flask(__name__)



import sentry_setup_routes, sentry_run_routes

#create cookies for new user

@app.route('/', methods=["GET"])
def entry_page():
	if request.method =="GET":
		resp = make_response(redirect(url_for('setup_sentry')))

		if not request.cookies.get('userid'):
			print("here")
			userid = ''.join(random.choices(string.ascii_uppercase+string.digits,k=64))
			resp.set_cookie('userid', userid, max_age=60*60*24*7)
			create_connection(f"{userid}.db")
			create_creds_and_whitelist_tables(f"{userid}.db")


	return resp


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')