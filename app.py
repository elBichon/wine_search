import flask
from flask import Flask, render_template, request, flash, session
import re
import os
import utils
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy 
import string


app = Flask(__name__, static_folder="static")
FILE = 'clean_wines3.csv'
STOP = ['suis', 'as', 'certaine', 'moindres', 'rien', 'tsoin', 'allô', 'quatre-vingt', 'hui', "d'", "d' ", 'néanmoins', 'lesquelles', 'dessous', 'revoilà', 'te', 'crac', 'lorsque', 'permet', 'sont', 'plutôt', 'subtiles', 'eux', 'parle', 'rarement', 'elle-même', 'tardive', 'nous-mêmes', 'o', 'toujours', 'elle', 'est', 'ce', 'directe', 'jusqu', 'celle-là', 'ohé', 'va', 'malgré', 'uniformement', 'excepté', 'mêmes', 'ouverts', 'comme', 'cinquantième', 'serait', 'pres', 'lès', 'étaient', "c'", 'nombreux', 'dite', 'juste', 'trente', 'puis', 'nul', 'pure', 'seulement', 'etc', 'sapristi', 'restrictif', 'sa', "m'", 'tellement', 'quatrièmement', 'même', 'tu', 'été', 'vais', 'exactement', 'avons', 'certains', 'delà', 'ouvert', 'necessairement', 'celui', 'je', 'las', 'dit', 'sept', 'aucune', 'soi-même', 'sauf', 'environ', 'stop', 'autres', 'feront', 'strictement', 'dix-huit', 'sur', 'naturelles', 'hi', 'pour', 'certaines', 'siennes', 'effet', 'absolument', 'nos', 'mille', 'suivant', 'le', 'necessaire', 'ore', 'entre', 'seraient', 'superpose', 'cinquantaine', 'plus', 'jusque', 'car', 'où', 'ça', 'tic', 'soit', 'zut', 'flac', 'sans', 'toute', 'et', 'lequel', 'eh', 'siens', 'possessif', 'seul', 'du', 'tres', 'ouias', 'sent', 'cependant', 'selon', 'comment', "l'", 'enfin', 'compris', 'telle', 'tente', "aujourd'hui", 'leur', 'probante', 'da', 'diverses', 'mon', 'encore', 'desormais', 'aie', 'paf', 'tenant', 'notre', 'était', 'plein', 'vifs', 'ceux', 'dessus', 'ceux-là', 'oust', 'quelle', 'possibles', 'neuvième', 'tous', 'i', 'divers', 'vous-mêmes', 'sera', 'qui', 'chacun', 'avais', 'pif', 'floc', 'comparable', 'ainsi', 'derniere', 'vôtres', 'parlent', 'tout', 'etais', 'm’', 'vas', 'quels', 'façon', 'desquels', 'c’', 'quoique', 'dix', 'moins', 'chères', 'sinon', 'differents', 'directement', 'hop', 'semble', 'onzième', 'rendre', 'cher', 'retour', 'toc', 'que', 'vu', 'brrr', 'fait', 'huitième', 'l’', 'souvent', 'allaient', 'chaque', 'ouf', 'uniques', 'pouvait', 'allo', 'd’', 'es', 'dring', 'peux', 'comparables', 'tac', 'celles', 'hum', 'reste', 'ta', 'la', 'soixante', 'extenso', 'exterieur', 'relativement', 'tes', 'aujourd', 'certes', 'font', 'bas', 'quelque', 'egale', "n'", 'fais', 'quand', 'bah', 'beau', 'seize', 'hein', 'speculatif', 'une', 'différentes', 'pouah', 'son', 'remarquable', 'na', 'sixième', 'sait', 'oh', 's’', 'moi-même', 'ouverte', 'suit', 'gens', 'psitt', 'elles', 'egales', 'pas', 'unes', 'ont', 'ces', 'six', 'aussi', 'rares', 'couic', 'avec', 'dernier', 'dix-neuf', 'pourrait', 'faisant', 'ci', "quelqu'un", 'aucun', 'moi-meme', 'doivent', 'notamment', 'diverse', 'par', 'tend', 'celle-ci', 'naturel', 'devant', 'naturelle', 'memes', 'dedans', 'neanmoins', 'treize', 'envers', 'seront', 'chiche', 'maint', 'douzième', 'premièrement', 'pourrais', 'fi', 'sous', 'rare', 'à', 'houp', 'celui-ci', 'duquel', 'surtout', 'j’', 'meme', 'partant', 'douze', 'avaient', 'lui', 'derriere', 'tsouin', 'sien', 'donc', 'a', 'ma', 'basee', 'plouf', 'personne', 'voici', 'hep', 'passé', 'dits', 'tienne', 'aurait', 'clic', 'suffisant', 'devers', 'les', 'parler', 'suivante', 'chère', 'me', 'anterieur', 'troisièmement', 'cinq', 'ne', 'ils', 'quatorze', 'dire', 'quant', 'avait', 'ait', 'probable', 'suivants', 'vif', 'pfft', 'neuf', 'restant', 'sienne', 'hélas', 'quarante', 'celle', 'pan', 'debout', 'sein', 'desquelles', 'ton', 'laquelle', 'etaient', 'pense', 'eux-mêmes', 'contre', 'hem', 'deux', 'té', 'vé', 'là', 'étais', 'relative', 'restent', 'pur', 'leurs', 'particulière', 'puisque', 'parfois', 'différent', 'cela', 'attendu', 'ha', 'miens', 'revoici', 'toi', 'tenir', 'celles-là', 'importe', 'depuis', 'celui-là', 'prealable', 'nous', 'vont', 'dans', 'maximale', 'auquel', 'hé', 'laisser', 'doit', 'merci', 'rend', 'deuxième', 'dehors', 'quelconque', 'hurrah', 'auxquels', 'allons', 'dès', 'nôtres', 'hou', 'étant', 'autre', 'parmi', 'abord', 'mienne', 'tiennes', 'ai', "j'", "qu'", 'pff', 'ayant', 't’', 'mais', 'plusieurs', 'on', 'pendant', 'alors', 'lors', 'pire', 'afin', 'apres', 'si', 'toi-même', 'unique', 'vôtre', 'toutefois', 'il', 'peu', 'quiconque', 'mince', 'quatre', 'dix-sept', 'non', 'ses', 'anterieure', 'ollé', 'quelles', 'egalement', 'un', 'nôtre', 'parseme', 'parce', 'assez', 'avant', 'olé', 'qu’', 'anterieures', 'vlan', "s'", 'semblaient', 'premier', 'de', 'suivre', 'au', 'huit', "t'", 'vers', 'première', 'possible', 'lui-meme', 'â', 'aura', 'holà', 'longtemps', 'ailleurs', 'très', 'ni', 'nombreuses', 'voilà', 'auraient', 'clac', 'mien', 'tant', 'autrefois', 'semblable', 'faisaient', 'aupres', 'cette', 'ho', 'désormais', 'touchant', 'devra', 'peuvent', 'telles', 'quelques', 'tiens', 'possessifs', 'malgre', 'certain', 'après', 'différents', 'chut', 'cinquième', 'seule', 'pourquoi', 'ah', 'bravo', 'toutes', 'n’', 'etait', 'ô', 'chers', 'ouste', 'autrement', 'procedant', 'quinze', 'quatrième', 'minimale', 'suffit', 'vivat', 'septième', 'se', 'vive', 'precisement', 'via', 'avoir', 'ès', 'hue', 'différente', 'près', 'auxquelles', 'quel', 'trop', 'specifique', 'trois', 'pfut', 'bat', 'moyennant', 'specifiques', 'cinquante', 'cet', 'euh', 'peut', 'bigre', 'troisième', 'en', 'different', 'tel', 'semblent', 'cent', 'nouveau', 'aux', 'chez', 'être', 'vous', 'miennes', 'vos', 'dixième', 'tien', 'etre', 'sacrebleu', 'ceux-ci', 'differentes', 'quant-à-soi', 'maintenant', 'auront', 'dont', 'combien', 'uns', 'moi', 'onze', 'autrui', 'bien', 'ou', 'suivantes', 'vingt', 'beaucoup', 'soi', 'elles-mêmes', 'mes', 'hors', 'suffisante', 'durant', 'quoi', 'eu', 'votre', 'vives', 'ceci', 'particulièrement', 'pu', 'derrière', 'concernant', 'deuxièmement', 'des', 'particulier', 'hormis', 'lui-même', 'proche', 'quanta', 'celles-ci', 'deja', 'chacune', 'lesquels', 'etant', 'boum', 'tels', 'outre']

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
				want = str(request.form["want"])
				want = utils.remove_stop_words(want, STOP)
				want = str(utils.process_request(want))
				answer = utils.generate_research_choice(df, couleur, pays)
				if len(want) > 0:
					answer = utils.treat_input(answer,want,'clean_text')
				else:
					pass
			else:
				pass
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


