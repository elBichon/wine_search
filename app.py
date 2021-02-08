
import flask
from flask import Flask, render_template, request, flash, session
import re
import utils
import spacy
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import *
import os


app = Flask(__name__, static_folder="static")
FILE = '../wines.csv'

answer = ""


@app.route("/search", methods=["POST"]) 
def upvote():
	send_msg = request.form["search"]
	answer = str(send_msg)
	print(answer)
	return str(answer)


@app.route("/")
def index():
	return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)


