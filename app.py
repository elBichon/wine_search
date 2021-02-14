
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
FILE = 'clean_wines.csv'

answer = ""


@app.route("/search", methods=["POST"]) 
def upvote():
	try:
		df = utils.read_data(FILE)
		if len(request.form["search_type"]) > 0 and isinstance(request.form["search_type"], str) == True and str(request.form["search_type"]) in ["label_choice", "name_choice", "research_choice"]:
			search_type = request.form["search_type"]
			if search_type == "label_choice":
				send_msg = request.form["wine_name"]
				answer = str(send_msg)
			elif search_type == "name_choice":
				answer = df.loc[df['name'] == str(request.form["wine_name"])]
				answer = answer[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description']].head(10)
			elif search_type == "research_choice":
				couleur = str(request.form["couleur"])
				pays = str(request.form["pays"])
				answer = utils.generate_research_choice(df, couleur, pays)
			else:
				answer = False
			return utils.generate_answer(answer)
		else:
			return False
	except:
		return False

@app.route("/")
def index():
	return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)


