import bs4 as bs
import urllib.request

url = input('enter hackerearth profile url - ')
sauce = urllib.request.urlopen(url).read()    
soup = bs.BeautifulSoup(sauce,'lxml')     # lxml is a parser
print(soup)

name = (soup.find('h1', class_="name ellipsis larger").text)
print(name)

followersNo = (soup.find('span', class_="track-followers-num").text)
followingNo = (soup.find('span', class_="track-following-num").text)
print("No. of followers = ",followersNo)
print("No. of following = ",followingNo)



##<!-- competitive coding data -->
##<div id="2915b83">
##</div>
##<!-- open source data -->
##<div id="2915bc4">
##</div>
