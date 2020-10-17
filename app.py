from flask import Flask, redirect, url_for, render_template, request, jsonify
import os
import cv2
import base64
import numpy as np
import json
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)

placeholder_img = os.path.join('static', 'images/placeholder.jpg')


port = 465  # For SSL
with open('sentry_email.json') as f:
	data = json.load(f)

sender_email = data["email"]
password = data["password"]

# Create a secure SSL context
context = ssl.create_default_context()


@app.route('/')
def hello_world():
	return redirect(url_for('setup_sentry'))

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

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		# Create a multipart message and set headers
		body = "Hey, you have requested to whitelist this person"
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = "Sentry is whitelisting this person !"

		# Add body to email
		message.attach(MIMEText(body, "plain"))

		filename = f"./static/images/captures/{name}.jpg"  # In same directory as script

		# Open PDF file in binary mode
		with open(filename, "rb") as attachment:
			# Add file as application/octet-stream
			# Email client can usually download this automatically as attachment
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())

		# Encode file in ASCII characters to send by email    
		encoders.encode_base64(part)

		# Add header as key/value pair to attachment part
		part.add_header(
		    "Content-Disposition",
		    f"attachment; filename= {image_name}",
		)

		# Add attachment to message and convert message to string
		message.attach(part)
		text = message.as_string()
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)

	#facial recognition operations
	response = 'whitelisted face'

	return response

	

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')