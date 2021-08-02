#----------------------------------------------------------------------
#   
#----------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import time
from datetime import datetime
import tzlocal
import html5lib

#================================================================================
#                         YAHOO FINANCE                                         #
#================================================================================
def getData_Yahoo(ticker):

    xList1 = []
    xList2 = []
    xList3 = []

    #---------------------  Populate List 1  ---------------------------

    try:

        # Rotate Dataframe 1st column as header
        df2 = pd.read_html(f'https://finance.yahoo.com/quote/{ticker}/')
        df2 = df2[1]
        df2 = df2.transpose()
        df2.columns = df2.iloc[0]
        df2 = df2[1:]
        print (tabulate(df2, headers='keys', tablefmt='psql', showindex=False))
     
        x1 = df2['Market Cap'].str.strip('[]')
        xMarketCap = x1.to_string(index=False)
        # print ("MarketCap: " + xMarketCap)

        x1 = df2['Beta (5Y Monthly)'].str.strip('[]')
        xBeta = x1.to_string(index=False)
        # print ("Beta (5Y Monthly): " + xBeta)

        x1 = df2['PE Ratio (TTM)'].str.strip('[]')
        xPERatio = x1.to_string(index=False)
        # print ("PE Ratio (TTM): " + xPERatio)

        x1 = df2['EPS (TTM)'].str.strip('[]')
        xEPS = x1.to_string(index=False)
        # print ("EPS (TTM): " + xEPS)

        x1 = df2['Earnings Date'].str.strip('[]')
        xEarningsDate = x1.to_string(index=False)
        # print ("Earnings Date: " + xEarningsDate)

        x1 = df2['Forward Dividend & Yield'].str.strip('[]')
        x1 = x1.to_string(index=False)
        xDividend = x1[:x1.find("(")-1]
        xYield = x1[x1.find("(")+1:-1]
        # print ("Dividend: " + xDividend)
        # print ("Yield: " + xYield)

        x1 = df2['Ex-Dividend Date'].str.strip('[]')
        xExDividendDate = x1.to_string(index=False)
        # print ("Ex-Dividend Date: " + xExDividendDate)

        x1 = df2['1y Target Est'].str.strip('[]')
        xTargetEst = x1.to_string(index=False)
        # print ("1y Target Est: " + xTargetEst)

        xList1.append(xMarketCap)
        xList1.append(xBeta)
        xList1.append(xPERatio)
        xList1.append(xEPS)
        xList1.append(xEarningsDate)
        xList1.append(xDividend)
        xList1.append(xYield)
        xList1.append(xExDividendDate)
        xList1.append(xTargetEst)

    except:
        xList1 = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        print ("Exception! YAHOO1")


    #---------------------  Populate List 2  ---------------------------

    recommendations = []
    url =   'https://query2.finance.yahoo.com/v10/finance/quoteSummary/' + \
            ticker + \
            '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'
    r = requests.get(url)
    if not r.ok:
        recommendation = 6
    try:
        result = r.json()['quoteSummary']['result'][0]
        # print (result)
        recommendation =result['financialData']['recommendationMean']['fmt']
        currentPrice =result['financialData']['currentPrice']['fmt']
        targetPrice =result['financialData']['targetMeanPrice']['fmt']
        upside = (float(targetPrice) - float(currentPrice)) / float(currentPrice) * 100
        xList2.append("$" + currentPrice)
        xList2.append("$" + targetPrice + " (" + str(round(upside)) + "%)")
        xList2.append(recommendation)
        xList2.append(str(result['recommendationTrend']['trend'][0]['strongBuy']))
        xList2.append(str(result['recommendationTrend']['trend'][0]['buy']))
        xList2.append(str(result['recommendationTrend']['trend'][0]['hold']))
        xList2.append(str(result['recommendationTrend']['trend'][0]['sell']))
        xList2.append(str(result['recommendationTrend']['trend'][0]['strongSell']))
        df = pd.DataFrame(xList2)
        # print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        # print (tabulate(df))
        df = df.transpose()
        df.columns = df.iloc[0]
        # df = df[1:]
        df.columns =['Current Price', 'Target Price', 'Analyst Recommendation', 'Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']
        print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))


    #---------------------  Populate List 3  ---------------------------

        for i in range(3):
            xTime = (result['upgradeDowngradeHistory']['history'][i]['epochGradeDate'])
            firm = (result['upgradeDowngradeHistory']['history'][i]['firm'])
            toGrade = (result['upgradeDowngradeHistory']['history'][i]['toGrade'])
            xTime = time.strftime('%Y-%m-%d', time.localtime(xTime))
            print ("Last Analysts Recommendation:         " + xTime + " " + firm + ": " + toGrade)
            xList3.append(xTime + " " + firm + ": " + toGrade)

    except:
        xList2 = ["-", "-", "-", "-", "-", "-", "-", "-"]
        xList3 = ["-", "-", "-"]
        print ("Exception! YAHOO2")
        recommendation = 6


    return xList1, xList2, xList3



#================================================================================
#                         STOCKINVEST                                           #
#================================================================================
def getData_StockInvest(ticker):

    xList = []

    url = "https://stockinvest.us/stock/" + ticker

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
        # soup = BeautifulSoup(page.text, 'html5lib') 
        soup = BeautifulSoup(page.text, 'lxml')

        # text = soup.get_text()
        # print (text)

        try:
            xScore = soup.find("div", {"class":"exampleDynamicGauge"}).get("data-value")
        except:
            xScore = 'N/A'

        try:
            xRating = soup.find("a", {"class":"btn btn-sm btn-secondary bg-success w-100p"}).text.strip()
        except:
            xRating = 'N/A'

        try:
            xLastAction = soup.find("a", {"class":"btn btn-sm btn-secondary }}"}).text.strip()
        except:
            xLastAction = 'N/A'

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
        except:
            xVolatility = 'N/A'

        try:
            x = soup.find_all("p", {"card-text my-auto"})
            x1 = x[2].text.strip()
            xResistance = 'N/A'
            if str(x1[0:13]) != 'No Resistance':
                xResistance = x1[x1.find("Resistance:")+12:x1.find("Price")-1]
            xPrice = x1[x1.find("Price:")+8:x1.find("Support")-1]
            xSupport = x1[x1.find("Support:")+10:]
            x2 = str(x[1])
            xRisk = x2[x2.find("badge white bg-"):]
            xRisk = xRisk[xRisk.find(">")+1:xRisk.find("<")]
        except:
            xResistance = 'N/A'
            xPrice = 'N/A'
            xSupport = 'N/A'
            xRisk = 'N/A'

# # Testing Only:
#         print("Score: " + xScore)
#         print("Rating: " + xRating)
#         print("Last Action: " + xLastAction)
#         print("Stop Loss: " + xStopLoss)
#         print("Target Price: " + xTarget)
#         print("Daily Average Volatility: " + xVolatility)
#         print("Resistance: " + xResistance)
#         print("Price: " + xPrice) 
#         print("Support: " + xSupport)
#         print ("Overall Risk: " + xRisk)

        xList = []
        xList.append(xScore)
        xList.append(xRating)
        xList.append(xLastAction)
        xList.append(xStopLoss)
        xList.append(xTarget)
        xList.append(xVolatility)
        xList.append(xResistance)
        xList.append(xPrice)
        xList.append(xSupport)
        xList.append(xRisk)
        df = pd.DataFrame(xList)
        df = df.transpose()
        df.columns = df.iloc[0]
        df.columns =['Score', 'Rating', 'Last Action', 'Stop Loss', 'Target', 'Volatility', 'Resistance', 'Price', 'Support', 'Risk']
        print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    # except IndexError:
    except:
        df = pd.DataFrame([])
        print ("Not Found Exception! - STOCKINVEST")
        pass


    return df



#================================================================================
#                         TIPRANKS                                              #
#================================================================================
def getData_Tipranks(ticker):

    xList = []

    url = "https://www.tipranks.com/stocks/" + ticker + "/forecast"

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
        soup = BeautifulSoup(page.text, 'lxml')
        # text = soup.get_text()
        # print (text)

        td = soup.find_all("span")
        currentPrice = (td[81].get_text()) 
        # print ("Current Price: " + currentPrice)

        td = soup.find_all(class_='colorpale fonth4_bold aligncenter mobile_mb0 mobile_fontSize3small w12')
        analystRating = (td[0].get_text()) 
        # print("Analyst Rating: " + analystRating) 

        td = soup.find_all(class_='h11 fontSize5')
        # print (td)
        totalRatings = (td[0].get_text())
        totalRatings = totalRatings.replace("Ratings","")
        # print("Total Ratings: " + totalRatings) 

        td = soup.find_all("div", class_="flexccc mt3 displayflex colorpale shrink0 lineHeight2 fontSize2 ml2 ipad_fontSize3")
        target = (td[0].get_text()) 
        targetPrice = target[:target.find("(")-1]
        # print ("Target Price: " + targetPrice)
        upside = target[target.find("(")-1:]
        # print ("Up/Down: " + upside)

        xList = []
        # xList.append(currentPrice)
        xList.append(analystRating)
        xList.append(totalRatings)
        xList.append(targetPrice)
        xList.append(upside)
        df = pd.DataFrame(xList)
        df = df.transpose()
        df.columns = df.iloc[0]
        df.columns =['Analyst Rating', 'Total Ratings', 'Target Price', 'Up/Down']
        print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))


    # except IndexError:
    except:
        df = pd.DataFrame([])
        print ("Not Found Exception! - TIPRANKS")
        pass


    return df



#================================================================================
#                         DIVIDATA                                              #
#================================================================================
def getData_Dividata(ticker):

    xList1 = []

    url = 'https://dividata.com/stock/' + ticker

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
        soup = BeautifulSoup(page.text, 'lxml')

        td = soup.find_all('span')
        xTicker = (td[10].get_text()) 
        sector = (td[8].get_text()) 
        industry = (td[9].get_text()) 
        lastClose = (td[11].get_text()) 
        payDate = (td[12].get_text()) 
        exDividendDate = (td[13].get_text()) 
        annualDividend = (td[14].get_text()) 
        annualYield = (td[15].get_text()) 
        lastDividend = (td[16].get_text()) 
        lastExDividendDate = (td[17].get_text()) 
        annualDividend = (td[18].get_text()) 
        dividendYield = (td[19].get_text()) 
        xList1.append(annualDividend)
        xList1.append(dividendYield)
        xList1.append(exDividendDate)
        xList1.append(payDate)
        xList1.append(lastDividend)

        td = soup.find_all(class_='progress')
        overallRating = str(td[0].get_text())
        dividendYield = str(td[1].get_text())
        dividendHistory = str(td[2].get_text())
        dividendStability = str(td[3].get_text())
        xList1.append(overallRating)
        xList1.append(dividendYield)
        xList1.append(dividendHistory)
        xList1.append(dividendStability)

        df1 = pd.DataFrame(xList1)
        df1 = df1.transpose()
        df1.columns = df1.iloc[0]
        df1.columns =['Annual\nDividend', 'Dividend\nYield', 'Ex-Dividend\nDate', 'Pay\nDate', 'Last\nDividend', 
            'Overall\nRating', 'Dividend\nYield', 'Dividend\nHistory', 'Dividend\nStability']
        print (tabulate(df1, headers='keys', tablefmt='psql', showindex=False))


    # except IndexError:
    except:
        df1 = pd.DataFrame([])
        print ("Not Found Exception! - DIVIDATA")
        pass


    return df1




#================================================================================
#                         ZACKS                                                 #
#================================================================================
def getData_Zacks(ticker):

    xList = []

    url = 'https://www.zacks.com/stock/quote/' + ticker

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
        soup = BeautifulSoup(page.text, 'lxml')

        x1 = soup.find("p", class_="rank_view").text.strip()
        xRank = x1[:x1.find(" ")]
        if "1-Strong" in xRank:
            xRank = xRank + " Buy"
        if "5-Strong" in xRank:
            xRank = xRank + " Sell"        # print ("Rank: " + xRank)
        x1 = soup.find_all("p", class_="rank_view")
        xIndustryRank = x1[2].text.strip()
        # print ("Industry Rank: " + xIndustryRank)
        xIndustry = x1[3].text.strip()
        xIndustry = xIndustry.replace("Industry: ","")
        # print ("Industry: " + xIndustry)
        xGrade = x1[1].text.strip()
        xGrade1 = xGrade[xGrade.find("Value")-2:xGrade.find("|")-7]
        # print ("Value Grade: " + xGrade1)
        xGrade2 = xGrade[xGrade.find("Growth")-2:xGrade.find("Growth")-1]
        # print ("Growth Grade: " + xGrade2)
        xGrade3 = xGrade[xGrade.find("Momentum")-2:xGrade.find("Momentum")-1]
        # print ("Momentum Grade: " + xGrade3)
        xGrade4 = xGrade[xGrade.find("VGM")-2:xGrade.find("VGM")-1]
        # print ("VGM Grade: " + xGrade4)

        xList = []
        xList.append(xRank)
        xList.append(xIndustryRank)
        xList.append(xIndustry)
        xList.append("<" + xGrade1 + ">")
        xList.append("<" + xGrade2 + ">")
        xList.append("<" + xGrade3 + ">")
        xList.append("<" + xGrade4 + ">")
        df = pd.DataFrame(xList)
        df = df.transpose()
        df.columns = df.iloc[0]
        df.columns =['Rank', 'Industry Rank', 'Industry', 'Value Grade', 'Growth Grade', 'Momentum Grade', 'VGM Grade']
        print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))



    # except IndexError:
    except:
        df = pd.DataFrame([])
        print ("Not Found Exception! - ZACKS")
        pass


    return df



#================================================================================
#                         MARKETWATCH                                           #
#================================================================================
def getData_MarketWatch(ticker):

    xList = []

    url = f'https://www.marketwatch.com/investing/stock/{ticker}/analystestimates?mod=mw_quote_tab'
    
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip', 
    'DNT' : '1', # Do Not Track Request Header 
    'Connection' : 'close'
    }

    try:

        page = requests.get(url, headers=headers) 
        soup = BeautifulSoup(page.text, 'lxml')

        #--------------------------  MARKETWATCH MARKET DATA  -----------------------------
        xMarket = soup.find('tbody', class_='markets__group')
        xMarket = xMarket.get_text()
        # print (xMarket)
        xMarket = xMarket.replace("\n", " ")
    
        if 'DJIA F' in xMarket:
            xMarketDow = xMarket[xMarket.find("DJIA F"):xMarket.find("%")+1]    
            xMarketDow = xMarketDow.replace("DJIA F", "DJIA")
        else:
            xMarketDow = xMarket[xMarket.find("Dow"):xMarket.find("%")+1]
        # print ("MarketWatch (Market Dow): " + xMarketDow)
        xMarketSNP = xMarket[xMarket.find("S&P"):]
        if 'S&P F' in xMarketSNP:
            xMarketSNP = xMarketSNP.replace("S&P F", "S&P")
        xMarketSNP = xMarketSNP.replace("S&P 500","S&P500")
        xMarketSNP = xMarketSNP[:xMarketSNP.find("%")+1]
        # print ("MarketWatch (Market S&P): " + xMarketSNP)
        if 'NASDAQ F' in xMarket:
            xMarketNasdaq = xMarket[xMarket.find("NASDAQ F"):]
            xMarketNasdaq = xMarketNasdaq.replace("NASDAQ F", "NASDAQ")
        else:
            xMarketNasdaq = xMarket[xMarket.find("Nasdaq"):]
        xMarketNasdaq = xMarketNasdaq[:xMarketNasdaq.find("%")+1]
        # print ("MarketWatch (Market Nasdaq): " + xMarketNasdaq)
        xMarketGold = xMarket[xMarket.find("Gold"):]
        xMarketGold = xMarketGold[:xMarketGold.find("%")+1]
        # print ("MarketWatch (Market Gold): " + xMarketGold)
        xMarketOil = xMarket[xMarket.find("Oil"):]
        xMarketOil = xMarketOil[:xMarketOil.find("%")+1]
        # print ("MarketWatch (Market Oil): " + xMarketOil)

        xMarketDow = xMarketDow.split()             # split string into list and remove any spaces
        xMarketSNP = xMarketSNP.split()             # split string into list and remove any spaces
        xMarketNasdaq = xMarketNasdaq.split()       # split string into list and remove any spaces
        xMarketGold = xMarketGold.split()           # split string into list and remove any spaces
        xMarketOil = xMarketOil.split()             # split string into list and remove any spaces

        xList = []
        xList.append(xMarketDow)
        xList.append(xMarketSNP)
        xList.append(xMarketNasdaq)
        df1 = pd.DataFrame(xList)
        df1.columns =['Market', 'Value', 'Change', 'Change %']
        print (tabulate(df1, headers='keys', tablefmt='psql', showindex=False))

        xList = []
        xList.append(xMarketGold)
        xList.append(xMarketOil)
        df2 = pd.DataFrame(xList)
        df2.columns =['Market', 'Value', 'Change', 'Change %']
        print (tabulate(df2, headers='keys', tablefmt='psql', showindex=False))

    except:
        df1 = pd.DataFrame([])
        df2 = pd.DataFrame([])
        print ("Not Found Exception! - MarketWatch DF1, DF2")
        pass

    try:
        #--------------------------  MARKETWATCH ANALYST RATINGS  -----------------------------
        xRatings = soup.find('table', class_='table table-primary align--left border--dotted')
        xRatings = xRatings.get_text()
        xRatings = xRatings.replace("\n", " ")
        xHeader = xRatings[xRatings.find("3M"):xRatings.find("Current")+7]
        xBuy = xRatings[xRatings.find("Buy"):xRatings.find("Overweight")]
        xOverweight = xRatings[xRatings.find("Overweight"):xRatings.find("Hold")]
        xHold = xRatings[xRatings.find("Hold"):xRatings.find("Underweight")]
        xUnderweight = xRatings[xRatings.find("Underweight"):xRatings.find("Sell")]
        xSell = xRatings[xRatings.find("Sell"):xRatings.find("Consensus")]
        xConsensus = xRatings[xRatings.find("Consensus"):]
        xBuy = xBuy.split()                         # split string into list and remove any spaces
        xOverweight = xOverweight.split()           # split string into list and remove any spaces
        xHold = xHold.split()                       # split string into list and remove any spaces
        xUnderweight = xUnderweight.split()         # split string into list and remove any spaces
        xSell = xSell.split()                       # split string into list and remove any spaces
        xConsensus = xConsensus.split()             # split string into list and remove any spaces
        xList = []
        xList.append(xBuy)
        xList.append(xOverweight)
        xList.append(xHold)
        xList.append(xUnderweight)
        xList.append(xSell)
        xList.append(xConsensus)
        df3 = pd.DataFrame(xList)
        # df = df.transpose()
        # df.columns = df.iloc[0]
        df3.columns =['Rating', 'Three_Month_Ago', 'One_Month_Ago', 'Current']
        df3 = df3[['Rating', 'Current', 'One_Month_Ago', 'Three_Month_Ago']]
        print (tabulate(df3, headers='keys', tablefmt='psql', showindex=False))


        #--------------------------  MARKETWATCH AFTER HOURS STOCK DATA  -----------------------------
        xAfterMarket = soup.find('h3', class_='intraday__price')
        xAfterMarket = xAfterMarket.get_text()
        xAfterMarket = xAfterMarket.replace("\n", " ")
        # print ("MarketWatch After Hours:       " + xAfterMarket)
        xAfterMarketChange = soup.find('span', class_='change--point--q')
        xAfterMarketChange = xAfterMarketChange.get_text()
        # print ("MarketWatch After Hours (+/-): " + xAfterMarketChange)
        xAfterMarketPerc = soup.find('span', class_='change--percent--q')
        xAfterMarketPerc = xAfterMarketPerc.get_text()
        xAfterMarketPerc = xAfterMarketPerc.replace("\n", " ")
        # print ("MarketWatch After Hours (%):   " + xAfterMarketPerc)
        xAfterMarketVolume = soup.find('div', class_='range__header')
        xAfterMarketVolume = xAfterMarketVolume.find('span', class_='primary')
        xAfterMarketVolume = xAfterMarketVolume.get_text()
        xAfterMarketVolume = xAfterMarketVolume.replace("Volume: ", "")
        # print ("MarketWatch After Hours (Volume): " + xAfterMarketVolume)
        xAfterMarketTime = soup.find('span', class_='timestamp__time')
        xAfterMarketTime = xAfterMarketTime.get_text()
        xAfterMarketTime = xAfterMarketTime.replace("Last Updated: ", "")
        # print ("MarketWatch After Hours (Time): " + xAfterMarketTime)    
        xMarketStatus = soup.find('div', class_='status')
        xMarketStatus = xMarketStatus.get_text()
        # print ("MarketWatch Market Status: " + xAfterMarketStatus)    

        xList = []
        xList.append(xAfterMarket)
        xList.append(xAfterMarketChange)
        xList.append(xAfterMarketPerc)
        xList.append(xAfterMarketVolume)
        xList.append(xAfterMarketTime)
        xList.append(xMarketStatus)
        df4 = pd.DataFrame(xList)
        df4 = df4.transpose()
        df4.columns = df4.iloc[0]
        df4.columns =['Price', 'Change', 'ChangePerc', 'Volume', 'AsofTime', 'MarketStatus']
        print (tabulate(df4, headers='keys', tablefmt='psql', showindex=False))


    except:
        df3 = pd.DataFrame([])
        df4 = pd.DataFrame([])
        print ("Not Found Exception! - MarketWatch DF3, DF4")
        pass


    return df1, df2, df3, df4




#================================================================================
#                Reddit Wall Street Bets Trending Stocks                        #
#================================================================================
def getData_Reddit():

    print("----------------------------------------------") 
    print("    Reddit Wall Street Bets Trending Stocks   ") 
    print("----------------------------------------------") 

    url = 'https://stocks.comment.ai/trending.html'

    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip', 
    'DNT' : '1', # Do Not Track Request Header 
    'Connection' : 'close'
    }

    local_time2 = ''
    try:

        page = requests.get(url, headers=headers) 
        # soup = BeautifulSoup(page.text, 'lxml')
        soup = BeautifulSoup(page.text, 'html5lib')
        # soup = BeautifulSoup(page, 'html.parser')
        # text = soup.get_text()


        test = soup.find("p", {"id": "unixtime_p"}).text.strip()
        test = test[11:]
        unix_timestamp = float(test)
        local_timezone = tzlocal.get_localzone() # get pytz timezone
        local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
        local_time2 = str(local_time)[:-6]

        trend_table = soup.find(class_='trending_table')

        df1 = pd.read_html(str(trend_table))
        df1 = df1[0]

        xRows = len(df1.index)
        xTotal = ''
        xBuy = ''
        xTicker = ''
        xList2 = []


        for index in range(xRows)[1:]:          # [1:] - To skip first row
            prices = soup.find_all("tr")
            xCntr = 1
            for x in prices[index].find_all("td"):  #.text.strip().split("\n")
                print ('x: ' + str(x))
                if xCntr == 1:
                    xTotal = str(x.get_text().strip())
                elif xCntr == 2:
                    xBuy = str(x.get_text().strip())
                elif xCntr == 3:
                    xTicker = str(x.get_text().strip())
                xCntr += 1

            x2 = str(x).replace("&amp;", "&")
            x2 = str(x).replace("&amp;", "&")

            xString = x2
            xCompany = xString[+4:xString.find("<br/>")]
            xIndustry = xString[xString.find("<br/>")+5:xString.find("</td>")]
            xBuyList = str(xBuy).split()             # split string into list and remove any spaces

            # print('Ticker: '+ str(xTicker))
            # print('Company: '+ str(xCompany))
            # print('Inductry: '+ str(xIndustry))
            # print('Buy: '+ xBuyList[0])
            # print('Sell: '+ xBuyList[1])
            # print('Hold: '+ xBuyList[2])
            # print('Total: '+ str(xTotal))

            xList = []
            xList.append(xTicker)
            xList.append(xCompany)
            xList.append(xIndustry)
            xList.append(xBuyList[0])
            xList.append(xBuyList[1])
            xList.append(xBuyList[2])
            xList.append(xTotal)
            xList2.append(xList) 

        df = pd.DataFrame(xList2)
        df.columns =['Ticker', 'Company', 'Industry', 'Buy', 'Sell', 'Hold', 'Total']
        print (tabulate(df, headers='keys', tablefmt='psql', showindex=False))


    # except IndexError:
    except:
        df = pd.DataFrame([])
        print ("Not Found Exception! - Reddit")
        pass


    return df, local_time2




#================================================================================
#                         MARKETWATCH ETFs                                          #
#================================================================================
def getData_MarketWatchETFs(ticker):

    url = f'https://www.marketwatch.com/investing/fund/{ticker}'
    
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip', 
    'DNT' : '1', # Do Not Track Request Header 
    'Connection' : 'close'
    }


    try:

        page = requests.get(url, headers=headers) 
        soup = BeautifulSoup(page.text, 'lxml')

        xDividendDate = ''
        xExpenseRatio = ''
        xTurnover = ''
        xBeta = ''
        xList1 = []
        xList2 = []

        x1 = soup.find('ul', class_='list list--kv list--col50')
        x2 = x1.find_all('li', class_='kv__item')
        for i in x2:
            x = i.get_text()
            x = x.replace("\n", " ")
            x = x[1:-2]
            xList1.append(x)
            if 'Net Expense Ratio' in x:
                xExpenseRatio = x[18:]
            if 'Beta' in x:
                xBeta = x[5:]
            if 'Turnover' in x:
                xTurnover = x[11:]
            if 'Ex-Dividend Date' in x:
                xDividendDate = x[17:]

        x1 = soup.find('ul', class_='list list--lipper')
        x2 = x1.find_all('li', class_='list__item')
        for i in x2:
            x = i.get_text()
            x = x.replace("\n", " ")
            # x = x[3:-1] + ': ' + x[1:2]
            x = x[1:2]
            xList2.append(x)

        print("xList1: " + str(xList1))
        print("xList2: " + str(xList2))
        print ("Beta: " + xBeta)
        print ("Expense Ratio: " + xExpenseRatio)
        print ("Turnover %: " + xTurnover)
        print ("Ex-Dividend Date: " + xDividendDate)


    except:
        print ("Not Found Exception! - MarketWatchETFs")
        pass


    return xBeta, xExpenseRatio, xTurnover, xDividendDate, xList2



#================================================================================
#                         DIVIDENDINVESTOR.COM                                  #
#================================================================================
def getData_DividendInvestor(ticker):

    url = f'https://www.dividendinvestor.com/dividend-quote/{ticker}/'
    
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'close'
    }


    try:

        page = requests.get(url, headers=headers) 
        soup = BeautifulSoup(page.text, 'lxml')

        xList1 = []
        x1 = soup.find('div', id='dividend-right')
        x2 = x1.find_all('span', class_='data')
        for i in x2:
            x = i.get_text()
            xList1.append(x)

        print("xList1: " + str(xList1))
        print("Dividend Ex Date: " + str(xList1[4]))
        print("Dividend Pay Date: " + str(xList1[6]))
        print("Dividend Frequency: " + str(xList1[9]))

    except:
        print ("Not Found Exception! - MarketWatchETFs")
        pass

    return str(xList1[4]), str(xList1[6]), str(xList1[9])



