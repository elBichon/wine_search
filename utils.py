import re
import spacy
import flask
from flask import Flask, render_template, request, flash, session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string


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
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description','clean_text']].head(10)
		elif couleur == 'no' and pays != 'no':
			df = df.loc[df['pays'] == pays]
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description','clean_text']].head(10)
		elif couleur != 'no' and pays == 'no':
			df = df.loc[df['couleur'] == couleur]
			answer = df[['name', 'image', 'pays','region', 'appelation', 'domaine', 'millesime', 'couleur','description','clean_text']].head(10)
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

def process_request(input_data):
	try:
		input_data = input_data.lower()
		input_data = input_data.replace(r"[^A-Za-z0-9éèçàùâêî]", " ")
		input_data = input_data.replace(" a ", " ")
		input_data = input_data.replace(" d ", " ")
		input_data = input_data.replace(" d' ", " ")
		input_data = input_data.replace(" d'", " ")
		input_data = input_data.replace(" l ", " ")
		input_data = input_data.replace(" s ", " ")
		input_data = input_data.replace(" c ", " ")
		input_data = input_data.replace(" i ", " ")
		input_data = input_data.replace(" y ", " ")
		input_data = input_data.replace(" à ", " ")
		input_data = input_data.replace(" n ", " ")
		input_data = input_data.replace(" n' ", " ")
		input_data = input_data.replace(" n'", " ")
		input_data = input_data.translate(str.maketrans('', '', string.punctuation))
		input_data = input_data.rstrip()
		input_data = input_data.lstrip()
		return input_data
	except:
		return False

def remove_stop_words(input_data, STOP):
	try:
		querywords = input_data.split()
		resultwords  = [word for word in querywords if word not in STOP]
		result = ' '.join(resultwords)
		return result
	except:
		return False

def get_data(df,column,query):
	try:
		vectorizer = TfidfVectorizer()
		X = vectorizer.fit_transform(df[column].values.tolist())
		print('a')
		vectorizer.fit(df[column].values.tolist())
		vector = vectorizer.transform([query])
		results = cosine_similarity(X,vector).reshape((-1,))
		df['grades'] = results
		print(df.grades)
		df = df.sort_values(by=['grades'], ascending=False)
		return df[['name', 'image', 'pays', 'region', 'appelation','domaine', 'millesime', 'couleur', 'description', 'clean_text']].head(2)
	except:
		pass


def treat_input(input_df,want,text):
	try:
		df_want = get_data(input_df,text,want)
		result_df = df_want
		return result_df
	except:
		pass