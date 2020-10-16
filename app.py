from flask import Flask, redirect, url_for, render_template
import os
import cv2

app = Flask(__name__)

placeholder_img = os.path.join('static', 'images/placeholder.jpg')


@app.route('/')
def hello_world():
	return redirect(url_for('setup_sentry'))

@app.route('/setup_sentry')
def setup_sentry():
	webcam = cv2.VideoCapture(0)
	# webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
	# webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

	if webcam.isOpened():
		_, frame = webcam.read()
		_, frame = cv2.imencode('.jpg', frame).tobytes()
		return render_template('sentry_setup_template.html', placeholder_img=frame)
	else:
		return render_template('sentry_setup_template.html', placeholder_img=placeholder_img)
	

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')