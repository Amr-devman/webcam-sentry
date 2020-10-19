from __main__ import app

from flask import Flask, redirect, url_for, render_template, request, jsonify


@app.route('/activate_sentry')
def activate_sentry():
	return 'placeholder'