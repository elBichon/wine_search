import bs4 as bs
import pandas as pd
from urllib.request import Request, urlopen
import urllib
import requests


df = pd.read_csv('wines.csv')
url = df.image.values.tolist()
i = 0

while i < len(url):
	name = str(i)+'.jpg'
	f = open(name,'wb')
	f.write(requests.get(url[i]).content)
	f.close()
	i += 1
