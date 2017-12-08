import os.path
from urllib.parse import quote, unquote
from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/texts')
def texts():
	return render_template('texts.html')

@app.route('/stats')
def ststs():
	return render_template('stats.html')

if __name__ == '__main__':
	app.run()#debug=True)
