from __main__ import app

from flask import Flask, redirect, url_for, render_template, request, jsonify
import base64
import cv2
import numpy as np
import os

from email_functions import send_image
from db_functions import select_query, insert_query, clear_whitelist_from_db, encode_arr
from face_recognition_functions import get_face_encodings


@app.route('/setup_sentry')
def setup_sentry():
	userid = request.cookies.get('userid')
	db_file = f"{userid}.db"
	results = select_query(db_file, ["email"], "creds")
	whitelist = select_query(db_file, ["name"],"whitelist")

	whitelisted_name = whitelist["name"].values

	#if there is a previous cred that was stored in the table, then autofill the
	#sentry mail feild, otherwise keep it empty
	if len(results):
		stored_cred = results["email"].values[-1]
	else:
		stored_cred = ""

	return render_template('sentry_setup_template.html', stored_cred=stored_cred, whitelisted_name=whitelisted_name)


@app.route('/_photo_cap', methods=["GET", "POST"])
def photo_cap():
	#get the 
	name = request.args.get('whitelisted_name')
	receiver_email = request.args.get('sentry_email')

	#update credintials if they are different than stored
	userid = request.cookies.get('userid')
	db_file = f"{userid}.db"
	results = select_query(db_file, ["email"], "creds")
	if len(results):
		stored_cred = results["email"].values[-1]
	else:
		stored_cred = ""

	if receiver_email != stored_cred:
		values = (receiver_email,)
		insert_query(db_file, ["email"], values ,"creds")


	photo_base64 = request.args.get('photo_cap')
	header, encoded = photo_base64.split(",", 1)
	binary_data = base64.b64decode(encoded)
	image_name = f"{name}.jpg"

	nparr = np.fromstring(binary_data, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

	whitelist_results = select_query(db_file, ["name"], "whitelist")
	whitelist_results = whitelist_results.values

	if name.lower() not in whitelist_results:
		#if a new peron is being whitelisted then we add him to the whitelist table,
		#else we ignore as we dont want duplicate entries
		values = (name.lower(), encode_arr(get_face_encodings(img_np)))
		insert_query(db_file, ["name", "embeddings"], values ,"whitelist")

		temp_img = os.path.join("./images/captures",image_name)
		with open(temp_img, "wb") as f:
			f.write(binary_data)

		send_image( receiver_email, subject="Sentry is whitelisting this person !",
					body="Hey, you have requested to whitelist this person",
					image_name=name)

		os.remove(temp_img)

	#facial recognition operations
	response = 'whitelisted face'

	return response

@app.route('/_clear_whitelist', methods=["GET", "POST"])
def clear_whitelist():
	'''
		clears whitelist when the user clicks the option
	'''
	userid = request.cookies.get('userid')
	db_file = f"{userid}.db"
	clear_whitelist_from_db(db_file, "whitelist")

	return jsonify("whitelist cleared")

	