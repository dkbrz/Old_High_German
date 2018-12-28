import os.path
from urllib.parse import quote, unquote
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, request, redirect, url_for
import pickle as pkl 
from collections import defaultdict
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)
TtoT = pkl.load(open('TtoT.pkl','rb'))
T = pkl.load(open('T.pkl','rb'))
R_INDEX = pkl.load(open('R_INDEX.pkl','rb'))
TEXTS = pkl.load(open('TEXTS.pkl','rb'))
DICT_INDEX = pkl.load(open('DICT_INDEX.pkl','rb'))
DICT_NODES = pkl.load(open('DICT_NODES.pkl','rb'))

def find_docs(words):
    all_indexes = [{} for _ in words]
    if len(words) > 0:
        result_t = set(R_INDEX[words[0]])
        all_indexes[0] = R_INDEX[words[0]]
        for key, i in enumerate(words[1:]):
            result_t = result_t & set(R_INDEX[i])
            all_indexes[key+1] = R_INDEX[i]
    else:
        result_t = set()
        
    #print (list(i.keys() for i in all_indexes))
    all_indexes = [{i:t[i] for i in t if i in result_t} for t in all_indexes]
    return result_t, all_indexes

def search_doc(docs, indexes, begin=-10, end=10):
    total = defaultdict(list)
    for key, value in enumerate(docs):
        variants = indexes[0][value]
        for i in variants:
            area = set(range(max(0, begin+i), i+end+1))
            result = set([i])
            k = 1
            for i in indexes[1:]:
                overlap = area & i[value]
                if len(overlap) > 0:
                    result.update(overlap)
                    k += 1
                else:
                    break
            if k == len(indexes):
                total[value].append(result)
    return dict(total)

def interpreter(result):
    sentences = []
    for text in result:
        for item in result[text]:
            left = max(0, min(item) - 20)
            right = max(item) + 20
            sentence = ''
            for i in range(left, right+1):
                if (text, i,) in TtoT:
                    token = TtoT[(text, i,)]
                    if i in item:
                        if token[1] is not None:
                            tooltipped = '<a href="#" data-toggle="tooltip" title="{}"> <font size="5"> {}</font> </a>'.format(token[1],token[0])
                        else:
                            tooltipped = '<font size="5">{} </font>'.format(token[0])
                        sentence = sentence + '<b>'+ tooltipped.replace('\n','<br>') +'</b>' + ' '
                    else:
                        if token[1] is not None:
                            tooltipped = '<a href="#" data-toggle="tooltip" title="{}">{} </a>'.format(token[1],token[0])
                        else:
                            tooltipped = '{} '.format(token[0])
                        sentence = sentence + tooltipped.replace('\n','<br>') + ' '
            sentences.append((TEXTS[text], sentence,))
    return sentences

def html_encoder(result):
    output = '<table border="2">'
    for i in result:
        output = output + '<tr><td width=20%>' + '</td><td>'.join(['<b>{}</b>'.format(i[0]), i[1]])+'</td></tr>'
    output += '</table>'
    return output

def dict_search(words):
    words = re.sub('[^\w ]','',words).split()
    if len(words) > 0:
        if words[0] in DICT_INDEX:
            result = DICT_INDEX[words[0]]
        else:
            result = set()
        for word in words:
            if word in DICT_INDEX:
                result = result & DICT_INDEX[word]
            else:
                result = set()
        result = [DICT_NODES[i] for i in sorted(result)]
        return result
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    if request.args:
        word = request.args['word']
        try:
                begin = -1*abs(int(request.args['begin']))
        except:
                begin = -10
        try:
                end = int(request.args['end'])
        except:
                end = 10
        words = word.split()
        try:
            R = interpreter(search_doc(*find_docs(words), begin=begin, end=end))
            R = html_encoder(R)
        except KeyError:
            R = '<table><tr><td>Nothing to show</td></tr></table>'
        return render_template('search.html', text=R)
    else:
        return render_template('search.html', text='<table><tr><td><b>Words:</b></td><td>please, enter words separated by space</td></tr><tr><td>\
<b>Begin:</b></td><td>search area on the left</td></tr><tr><td><b>End:</b></td><td>search area on the right</td></tr></table>')


@app.route('/texts')
def texts():
    return render_template('texts.html')


@app.route('/dictionary', methods=['GET'])
def dictionary():
    if request.args:
        result = dict_search(request.args['words'])
        if len(result) > 0:
            result = '<table style="border-bottom: 1px !important;" ><tr><td>{}</td></tr></table>'.format('</td></tr><tr><td>'.join(result))
        else:
            result = '<table><tr><td>No results</td></tr></table>'
        return render_template('dictionary_search.html', result=result)
    else:
        return render_template('dictionary.html')

@app.route('/stats')
def stats():
	return render_template('stats.html')


@app.route('/about')
def about():
	return render_template('about.html')

# Text pagess
@app.route('/tatian')
def tatian():
	return render_template('tatian.html')
@app.route('/eide')
def eide():
	return render_template('eide.html')
@app.route('/wessobrunner')
def wessobrunner():
	return render_template('wessobrunner.html')
@app.route('/isidor')
def isidor():
	return render_template('isidor.html')
@app.route('/merseburger1')
def merseburger1():
	return render_template('merseburger1.html')
@app.route('/merseburger2')
def merseburger2():
	return render_template('merseburger2.html')
@app.route('/muspilli')
def muspilli():
	return render_template('muspilli.html')
@app.route('/hildebrandslied')
def hildebrandslied():
	return render_template('hildebrandslied.html')
@app.route('/glossen')
def glossen():
	return render_template('glossen.html')
@app.route('/evangelienbuch')
def evangelienbuch():
	return render_template('evangelienbuch.html')
@app.route('/physyologus')
def physyologus():
	return render_template('physyologus.html')
@app.route('/ludwigslied')
def ludwigslied():
	return render_template('ludwigslied.html')
@app.route('/notker')
def notker():
	return render_template('notker.html')


if __name__ == '__main__':
    app.run()
	#app.run(debug=True)
