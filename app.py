from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
	return redirect(url_for('setup_sentry'))

@app.route('/setup_sentry')
def setup_sentry():
	return 'Hello, World!'
	

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')