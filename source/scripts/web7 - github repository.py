import bs4 as bs
import urllib.request

url = input('enter github url - ')
sauce = urllib.request.urlopen(url).read()    
soup = bs.BeautifulSoup(sauce,'lxml')     # lxml is a parser

n = int(soup.find('span',class_='Counter').text)
print("no. of repositories = "+str(n))
print()
tags = soup.find_all('a')
for tag in tags:
    print(tag.get('href'))
