import sys
#importing PyQt is widely used for developing graphical interfaces , helps to get dynamic data
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
#importing Beautiful soup module which is Best for web scrapping using python 
import bs4 as bs
import urllib.request

class Client(QWebPage):
#acess the url and Get the Data when Page load Completes
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
        
    def on_page_load(self):
        self.app.quit()
 #url for particular profile       
url = 'https://www.hackerearth.com/@code_sirens_tri'
client_response = Client(url)
source = client_response.mainFrame().toHtml()
soup = bs.BeautifulSoup(source, 'lxml')

#For getting the Desired Data
solved = soup.find_all('span', class_='dark weight-700')
rating = soup.find_all('a', class_='dark weight-700')
print("Problem Solved")
print(solved[0].string)
print("Rating")
print(rating[0].string)