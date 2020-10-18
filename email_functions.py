import json
import smtplib, ssl
import base64

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_context_and_creds(secret_file='sentry_email.json', port=465):
	port = 465  # For SSL
	with open(secret_file) as f:
		data = json.load(f)

	sender_email = data["email"]
	password = data["password"]

	# Create a secure SSL context
	context = ssl.create_default_context()

	return sender_email, password, port, context


def send_image(receiver_email, subject, body, image_name):
	sender_email, password, port, context = get_context_and_creds()

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		# Create a multipart message and set headers
		body = body
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = subject

		# Add body to email
		message.attach(MIMEText(body, "plain"))

		filename = f"./static/images/captures/{image_name}.jpg"  # In same directory as script

		# Open image file in binary mode
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
		    f"attachment; filename= {image_name}.jpg",
		)

		# Add attachment to message and convert message to string
		message.attach(part)
		text = message.as_string()
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)
