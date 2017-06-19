import bs4 as bs
import urllib.request
import pandas as pd

url = input('enter - ')
dfs = pd.read_html(url, header=0)
for df in dfs:
    print (df)
