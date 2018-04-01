import os.path
from urllib.parse import quote, unquote
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, request, redirect, url_for


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/search')
def search():
	return render_template('search.html')


@app.route('/texts')
def texts():
	return render_template('texts.html')


@app.route('/dictionary')
def dictionary():
	return render_template('dictionary.html')


@app.route('/stats')
def stats():
	return render_template('stats.html')


@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/glossen')
def glossen():
	return render_template('glossen.html')

if __name__ == '__main__':
    app.run()
	#app.run(debug=True)
