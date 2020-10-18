from flask import Flask, redirect, url_for, render_template, request, jsonify
import os

app = Flask(__name__)



import sentry_setup_routes


@app.route('/')
def entry_page():
	return redirect(url_for('setup_sentry'))


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')