
# Scrapes the data from codechef and goves out the RAting, Global&Country Rankings
import requests
from bs4 import BeautifulSoup

head = "https://wwww.codechef.com/users/"
var = "ravi_7"
URL = head + var

page  = requests.get(URL)
soup = BeautifulSoup(page.content,'html.parser')

#These three lines give the Rating of the user.
listRating = list(soup.findAll('div',class_="rating-number"))
rating = list(listRating[0].children)
rating = rating[0]
print "Rating: "+rating

listGCR = []  #Global and country ranking.
listRanking = list(soup.findAll('div',class_="rating-ranks"))
rankingSoup = listRanking[0] 
for item in rankingSoup.findAll('a'):
	listGCR.append(item.get_text()) #Extracting the text from all anchor tags
print "Global Ranking: "+listGCR[0]
print "Country Ranking: "+listGCR[1]
