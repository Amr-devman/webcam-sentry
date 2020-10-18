from __main__ import app

from flask import Flask, redirect, url_for, render_template, request, jsonify
import base64
import cv2
import numpy as np
import os

from email_functions import send_image


placeholder_img = os.path.join('static', 'images/placeholder.jpg')


@app.route('/setup_sentry')
def setup_sentry():
	return render_template('sentry_setup_template.html', placeholder_img=placeholder_img)


@app.route('/_photo_cap', methods=["GET", "POST"])
def photo_cap():
	name = request.args.get('whitelisted_name')
	receiver_email = request.args.get('sentry_email')

	photo_base64 = request.args.get('photo_cap')
	header, encoded = photo_base64.split(",", 1)
	binary_data = base64.b64decode(encoded)
	image_name = f"{name}.jpg"

	nparr = np.fromstring(binary_data, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
	with open(os.path.join("./static/images/captures",image_name), "wb") as f:
		f.write(binary_data)

	send_image( receiver_email, subject="Sentry is whitelisting this person !",
				body="Hey, you have requested to whitelist this person",
				image_name=name)

	#facial recognition operations
	response = 'whitelisted face'

	return response