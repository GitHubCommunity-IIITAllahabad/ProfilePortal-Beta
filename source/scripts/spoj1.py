from bs4 import BeautifulSoup
import requests

base = "https://spoj.com/users/"
var = "ravi_7"
#var = raw_input('Enetr your Username')
url = base + var
sauce = requests.get(url) 
soup = BeautifulSoup(sauce.content,'lxml')     # lxml is a parser
#print(soup.prettify())
iList = []
info = (soup.find_all('p'))
for i in info:
    iList.append(i.text)
print iList[2] #World rank
print iList[3] #Institution

no_of_questions = int(soup.find('dd').text)
print(" no. of questions = ",no_of_questions)
