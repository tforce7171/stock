import pandas as pd
import pandas_datareader.data as web
import datetime
import requests
from bs4 import BeautifulSoup
import json
import re
# import matplotlib.pyplot as plt

global headers
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15 "}


def LoopPages():
    # url = "https://kabuoji3.com/stock/?page=1"
    # hash = ScrapeTickers(url)
    pages = list(range(1,34))
    hash = {}
    for page in pages:
        url = "https://kabuoji3.com/stock/?page={page}".format(page=page)
        hash.update(ScrapeTickers(url))
    hash_to_json = json.dumps(hash)
    file = open('stock_data.json','w')
    json.dump(hash_to_json,file,indent=4)
def ScrapeTickers(url):
    print url
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.content,"html.parser")
    table = soup.find_all("table", {"class":"stock_table"})[0]
    trs = table.find_all("tr")
    del trs[0]
    hash = {}
    for tr in trs:
        url = tr.get("data-href")
        print url
        hash.update(ScrapeYears(url))
    return hash
def ScrapeYears(url):
    print url
    ticker = str(re.findall('https://kabuoji3.com/stock/(.*)/', url)[0])
    print ticker
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.content,"html.parser")
    years = soup.find("ul",{"class":"stock_yselect mt_10"}).find_all("a")
    del years[0]
    hash_ticker = {}
    hash_year = {}
    for year in years:
        url = year.get("href")
        hash_year.update(ScrapeStockData(url))
    hash_ticker[ticker] = hash_year
    return hash_ticker
def ScrapeStockData(url):
    print url
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.content,"html.parser")
    table = soup.find("table", {"class":"stock_table stock_data_table"})
    rows = table.find_all("tr")
    del rows[0]
    hash_date = {}
    for row in rows:
        datas = row.find_all("td")
        hash_data = {}
        hash_data["open_price"] = datas[1].get_text()
        hash_data["high_price"] = datas[2].get_text()
        hash_data["low_price"] = datas[3].get_text()
        hash_data["closing_price"] = datas[4].get_text()
        hash_data["volume"] = datas[5].get_text()
        hash_data["adjusted_closing_price"] = datas[6].get_text()
        hash_date[datas[0].get_text()] = hash_data
    return hash_date

LoopPages()
