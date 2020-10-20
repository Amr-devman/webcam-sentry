from __main__ import app

from flask import Flask, redirect, url_for, render_template, request, jsonify

import cv2
import numpy as np
import os
import base64
import imutils

from email_functions import send_image
from db_functions import select_query
from face_recognition_functions import detect_and_match_faces



@app.route('/activate_sentry')
def activate_sentry():
	return render_template('sentry_run_template.html')


@app.route('/_motion_detection', methods=["GET", "POST"])
def _motion_detection():
	userid = request.cookies.get('userid')
	
	#file path for the first frame
	prev_img_file = f"{userid}_prev_img.npy"
	prev_img_filepath = os.path.join("./prev_images", prev_img_file)

	#accessing user's db
	db_file = f"{userid}.db"
	results = select_query(db_file, ["email"], "creds")
	receiver_email = results["email"].values[-1]

	photo_base64 = request.args.get('photo_cap')
	header, encoded = photo_base64.split(",", 1)
	binary_data = base64.b64decode(encoded)

	nparr = np.fromstring(binary_data, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

	gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
	gray = cv2.GaussianBlur(gray, (11,11), 0)


	if prev_img_file not in os.listdir("./prev_images"):
		np.save(prev_img_filepath, gray)

	#find the difference between the prev frame and current frame
	first_frame = np.load(prev_img_filepath)

	frame_delta = cv2.absdiff(first_frame, gray)
	thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

	#dialate image to fill holes and find contours
	thresh = cv2.dilate(thresh, None, iterations=2)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)

	suspects = []

	for idx, c in enumerate(contours):
		if cv2.contourArea(c) < 100:
			continue
		else:
			(xmin, ymin, width, height) = cv2.boundingRect(c)
			img_np_copy = img_np.copy()
			unmatched = detect_and_match_faces(img_np_copy[ymin:ymin+height, xmin:xmin+width, :], userid)
			if (unmatched != 0) and (unmatched != -99):
				suspects.append(img_np_copy[ymin:ymin+height, xmin:xmin+width, :])

				if len(suspects) > 0:
					temp_file_path = os.path.join("./images/captures",f"suspect_{idx}.jpg")

					temp_img = cv2.cvtColor(img_np_copy[ymin:ymin+height, xmin:xmin+width, :], cv2.COLOR_BGR2RGB)
					cv2.imwrite(temp_file_path, temp_img)
					send_image( receiver_email,
								"Sentry Alert",
								"An unidentified person was spotted by the sentry",
								f"suspect_{idx}")

					os.remove(temp_file_path)

	np.save(prev_img_filepath, gray)
	return jsonify("Detection done")








