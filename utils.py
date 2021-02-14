import re
import spacy
import flask
from flask import Flask, render_template, request, flash, session
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_data(text):
	try:
		if len(str(text)) > 0 and isinstance(text, str) == True:
			#nlp = en_core_web_sm.load()
			nlp = spacy.load('en_core_web_sm')
			nlp.max_length = 1500000
			stemmer = SnowballStemmer(language='english')
			text = remove_stopwords(text).lower()
			text = (re.sub("[^a-zA-Z]"," ",text)).rstrip().lstrip()
			return text
		else:
			return False
	except:
		return False


def get_data(df,text,query):
	try:
		if len(str(query)) > 0 and isinstance(query, str) == True and len(str(text)) > 0 and isinstance(text, list) == True:
			vectorizer = TfidfVectorizer()
			X = vectorizer.fit_transform(text)
			vectorizer.fit(text)
			vector = vectorizer.transform([query])
			results = cosine_similarity(X,vector).reshape((-1,))
			df['grades'] = results
			df = df.sort_values(by=['grades'], ascending=False)
			return df[['title','recommendations','artist','publisher','writer','genres','summary']].head(100)
		else:
			return False
	except:
		return False


def read_data(dataset):
	try:
		if len(str(dataset)) > 0 and isinstance(dataset, str) == True:
			df = pd.read_csv(dataset)
			if len(df) > 0 and isinstance(df, pd.DataFrame) == True:
				return df
			else:
				return False
		else:
			return False
	except:
		return False


def generate_research_choice(df, couleur, pays):
	try:
		if couleur != 'no' and pays != 'no':
			df = df.loc[df['couleur'] == couleur]
			df = df.loc[df['pays'] == pays]
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description']].head(10)
		elif couleur == 'no' and pays != 'no':
			df = df.loc[df['pays'] == pays]
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description']].head(10)
		elif couleur != 'no' and pays == 'no':
			df = df.loc[df['couleur'] == couleur]
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description']].head(10)
		elif couleur == 'no' and pays == 'no':
			answer = 'void'
		else:
			answer = False
		return answer
	except:
		return False


def generate_answer(answer):
	try:
		i = 0
		separator = ','
		generated_answer = []
		while i < len(answer.values.tolist()):
			generated_answer.append('<div><img src='+str(answer.values.tolist()[i][1])+'></br><strong>Nom: </strong>'+str(answer.values.tolist()[i][0])+'</br>'+'<strong>Pays: </strong>'+str(answer.values.tolist()[i][2])+'</br>'+'<strong>Region: </strong>'+str(answer.values.tolist()[i][3])+'</br>'+'<strong>Appelation: </strong>'+str(answer.values.tolist()[i][4])+'</br>'+'<strong>Domaine: </strong>'+str(answer.values.tolist()[i][5])+'</br>'+'<strong>Millesime: </strong>'+str(answer.values.tolist()[i][6])+'</br>'+'<strong>Couleur: </strong>'+str(answer.values.tolist()[i][7])+'</br><p>'+str(answer.values.tolist()[i][8])+'</p></div></br></br>')
			i += 1
		return str(separator.join(generated_answer))
	except:
		return False

