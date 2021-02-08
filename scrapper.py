import bs4 as bs
import pandas as pd
from urllib.request import Request, urlopen


srce_url = 'https://www.wineandco.com/search?term=&sort=relevance&paginationLength=1600&pageNumber='
i = 1
urls = []
while i <= 6:
	url = srce_url+str(i)
	print(url)
	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		response = urlopen(req, timeout=60).read()
		soup = bs.BeautifulSoup(response,'lxml')		
		for url in soup.find_all('a',class_='push-product'):
			urls.append('https://www.wineandco.com'+str(url.get('href')))
	except:
		pass
	i += 1



print(len(urls))
urls = list(set(urls))
print(len(urls))

start = 'href="'
end = '">'

pays = []
name = []
region = []
appelation = []
domaine = []
millesime = []
couleur = []
image = []
wine_description = []

for url in urls:
	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		response = urlopen(req, timeout=20).read()
		soup = bs.BeautifulSoup(response,'lxml')
		l = str(soup.find_all('span',class_='caract-data')).replace('<span class="caract-data" itemprop="category">','').replace('</span>','').replace('\n','').replace('[','').replace(']','').split(',')
		s = str(soup.find('div',class_='popup_gal_item'))
		description = str(soup.find('div',class_='wine_description').get_text().replace('\r','').replace('\n',''))
		if len(l) == 9:
			pays.append(l[0])
			region.append(l[1])
			appelation.append(l[2])
			domaine.append(l[3])
			millesime.append(l[6])
			couleur.append(l[8])
			name.append(soup.h1.get_text())
			wine_description.append(description)
			image.append(str((s.split(start))[1].split(end)[0]))
		elif len(l) == 10:
			pays.append(l[0])
			region.append(l[1])
			appelation.append(l[2])
			domaine.append(l[3])
			millesime.append(l[6])
			couleur.append(l[9])
			name.append(soup.h1.get_text())
			wine_description.append(description)
			image.append(str((s.split(start))[1].split(end)[0]))
		elif len(l) == 8:
			pays.append(l[0])
			region.append(l[1])
			appelation.append(l[2])
			domaine.append(l[3])
			millesime.append(l[6])
			couleur.append(l[7])
			name.append(soup.h1.get_text())
			wine_description.append(description)
			image.append(str((s.split(start))[1].split(end)[0]))
		elif len(l) == 7:
			pays.append(l[0])
			region.append(l[1])
			appelation.append(l[2])
			domaine.append(l[3])
			millesime.append(l[6])
			couleur.append(l[6])
			name.append(soup.h1.get_text())
			wine_description.append(description)
			image.append(str((s.split(start))[1].split(end)[0]))
		else:
			print(len(l))
			print(url)
			pass
	except:
		pass

data = {'name':name,'image':image,'pays':pays,'region':region,'appelation':appelation,'domaine':domaine,'millesime':millesime,'couleur':couleur,'description':wine_description}
df = pd.DataFrame.from_dict(data)
df.to_csv('wines.csv')
