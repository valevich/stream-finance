import pandas as pd
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf 
import os
import pygsheets
from google.oauth2 import service_account
import urllib.request, json 
import time
from lxml import html


#---------------------------------------------------------------------------------------#
#-                         CURRENT STOCK PRICES AND STOP/LOSS                           #
#---------------------------------------------------------------------------------------#
def getData_stockinvest():

    print ('------------------------------------------------------')
    print ('    START stock_scrape2.py - getData_stockinvest()    ')
    print ('------------------------------------------------------')

    is_prod = os.environ.get('IS_HEROKU', None)

    if is_prod:
        gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env variable
    else:    
        gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials

    xList2 = []

    ##### TESTING ONLY ####
    # xList3 = ['MSFT','AAPL','MO']
    # for i in xList3:
    #     symbol = i
    #     print (symbol)
    #     xCurrentStopLoss = '6.00*'
    #     xList = getData_ticker(symbol, xCurrentStopLoss)
    #     xList2.append(xList)
    ##### TESTING ONLY ####

    ##### TESTING ONLY ####
    # sheet = gc.open('Research')
    # wks = sheet.worksheet_by_title('Portfolio')
    # df1 = wks.get_as_df()
    # for index, row in df1.iterrows():
    #     if row[1] != 'Ticker' and row[1] != 'CASH':
    #         symbol = row[1]
    #         xCurrentStopLoss = row[6] + ' (-' + row[7] + ')'
    #         xList = getData_ticker(symbol, xCurrentStopLoss)
    #         xList2.append(xList)
    ##### TESTING ONLY ####

    ##### LIVE ####
    sheet = gc.open('Research')
    wks = sheet.worksheet_by_title('Portfolio')
    for row in wks:
        if row[1] != 'Ticker' and row[1] != 'CASH':
            symbol = row[1]
            xCurrentStopLoss = row[6] + ' (-' + row[7] + ')'
            xList = getData_ticker(symbol, xCurrentStopLoss)
            xList2.append(xList)
    ##### LIVE ####

    return xList2



def getData_ticker(symbol, xCurrentStopLoss):
    xList = []

    url = "https://stockinvest.us/stock/" + symbol

    try:
        headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'close'
        }
        page = requests.get(url, headers=headers)
        soup = bs(page.text, 'lxml')
        # print (soup)

    except:
        print ("Not Found Exception! - STOCKINVEST")

    try:
        xScore = soup.find("div", {"class":"exampleDynamicGauge"}).get("data-value")
    except:
        xScore = 'N/A'

    try:
        x1 = soup.find("span", {"class":"btn-group w-100p"}).text.strip()
        x1 = x1.split('\n')
        # print (x1)
        xRating = x1[0]
        xLastAction = x1[3]
        # print (xRating)
        # print (xLastAction)
    except:
        xRating = 'N/A'


    try:
        xStopLoss = soup.find("span", {"font-weight-400 float-right"}).text.strip()
    except:
        xStopLoss = 'N/A'

    try:
        xTarget = soup.find_all("td", {"grey-800 text-center"})
        xTarget = xTarget[1].text.strip()
    except:
        xTarget = 'N/A'

    try:
        xVolatility = soup.find("span", {"card-text my-auto"}).text.strip()
        xVolatility = xVolatility[:-25]
        xVolatility = xVolatility.replace(" ", "")
    except:
        xVolatility = 'N/A'

    try:
        x = soup.find_all("p", {"card-text my-auto"})
        x1 = x[2].text.strip()
        x2 = str(x[1])
        xRisk = x2[x2.find("badge white bg-"):]
        xRisk = xRisk[xRisk.find(">")+1:xRisk.find("<")]
    except:
        xRisk = 'N/A'


    url = f'https://www.marketwatch.com/investing/stock/{symbol}/analystestimates?mod=mw_quote_tab'
    page = requests.get(url, headers=headers) 
    soup = bs(page.text, 'lxml')
    xPrice = soup.find_all('div', class_='intraday__data')
    xPrice = xPrice[0].get_text()
    xPrice = xPrice.replace("\n", " ")
    xPrice = xPrice.split()
    xPrice = xPrice[0] + xPrice[1] + ' (' + xPrice[3] + ')'
    print (symbol + ': ' + xPrice)

    if '%' in xCurrentStopLoss:
        x1 = xCurrentStopLoss[xCurrentStopLoss.find('(')+1:xCurrentStopLoss.find('%')]
        x1 = x1.replace('-','')
        x1 = float(x1)
        if x1 > 5.00:
            xCurrentStopLoss = xCurrentStopLoss + '*'
    

    xList = []
    xList.append(symbol)
    xList.append(xScore)
    xList.append(xRating)
    xList.append(xLastAction)
    xList.append(xPrice)
    xList.append(xCurrentStopLoss)
    xList.append(xStopLoss)
    xList.append(xVolatility)
    xList.append(xRisk)


    return xList





