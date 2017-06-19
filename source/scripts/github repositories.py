import bs4 as bs
import urllib.request

username = input('enter github username - ')
url = "https://github.com/"+username
sauce = urllib.request.urlopen(url).read()    
soup = bs.BeautifulSoup(sauce,'lxml')     # lxml is a parser
print(soup)

repoNo = int(soup.find('span',class_='Counter').text)
n1 = repoNo

url2 = url + "?tab=repositories"
sauce = urllib.request.urlopen(url2).read()    
soup = bs.BeautifulSoup(sauce,'lxml')
#print(soup)

arr = [0]
tags = soup.find_all('a', itemprop="name codeRepository")
for tag in tags:
    if tag.text!="":
        arr.append((tag.text).lstrip())

k=2
while(len(arr)<=n1):
    url3 = url + "?page="+str(k)+"&tab=repositories"
    k+=1
    sauce = urllib.request.urlopen(url3).read()    
    soup = bs.BeautifulSoup(sauce,'lxml')
    tags = soup.find_all('a', itemprop="name codeRepository")
    for tag in tags:
        if tag.text!="":
            arr.append((tag.text).lstrip())

for i in range(1,len(arr)):
    h1 = str(i) + ".  "+str(arr[i])
    print(h1) 
