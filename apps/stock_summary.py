import streamlit as st 
import os
import requests
import yfinance as yf 
import plotly.graph_objects as go 
import plotly.express as px 
from plotly.subplots import make_subplots
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from bs4 import BeautifulSoup
import datetime
import cufflinks as cf
from datetime import date
import markdown
import pygsheets
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
from gsheetsdb import connect

from apps.stock_scrape1 import getData_Zacks
from apps.stock_scrape1 import getData_Dividata
from apps.stock_scrape1 import getData_Tipranks
from apps.stock_scrape1 import getData_StockInvest
from apps.stock_scrape1 import getData_MarketWatch
from apps.stock_scrape1 import getData_MarketWatchETFs
from apps.stock_scrape1 import getData_MarketWatchDividends


def app():

    is_prod = os.environ.get('IS_HEROKU', None)

    st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)    


    #------ Function to DISPLAY SUMMARY (STOCKS) ----------
    def display_summary_equity(symbol,rowNo):

        try:
            xPrice = "%0.2f" % (ticker.info['currentPrice'])                    # force display two decimals
            xPrevClose = "%0.2f" % (ticker.info['previousClose'])               # force display two decimals
            xOpen = "%0.2f" % (ticker.info['open'])                             # force display two decimals
            xChange = "%0.2f" % (float(xPrice) - float(xPrevClose))
            xChangePerc = "%0.2f" % ((float(xPrice) - float(xPrevClose)) / float(xPrevClose) * 100)
            xFiftyTwoWeekRange = str("%0.2f" % ticker.info['fiftyTwoWeekLow']) + ' - ' + str("%0.2f" % ticker.info['fiftyTwoWeekHigh'])
            xMarketCap = human_format(ticker.info['marketCap'])
            if ticker.info['dividendRate']:
                xDividendRate = ticker.info['dividendRate']
                xDividendYield = str("%0.2f" % (float(xDividendRate) / float(xPrice) * 100))
                xDividend = str(xDividendRate) + ' (' + str(xDividendYield) + '%)'
            else:
                xDividend = '-'
            if 'trailingPE' in ticker.info:
                xTrailingPE = "%0.2f" % ticker.info['trailingPE']
            else:
                xTrailingPE = '-'
            if 'trailingEps' in ticker.info:
                if ticker.info['trailingEps']:
                    xTrailingEps = "%0.2f" % ticker.info['trailingEps']
                else:
                    xTrailingEps = '-'
            else:
                xTrailingEps = '-'
            xVolume = human_format(ticker.info['volume'])

            if len(df_mw4) > 0:
                xAfterMarketPrice = df_mw4.iloc[0]['Price']
                xAfterMarketChange = df_mw4.iloc[0]['Change']
                xAfterMarketPerc = df_mw4.iloc[0]['ChangePerc']
                xAfterMarketVolume = df_mw4.iloc[0]['Volume']
                xAfterMarketTime = df_mw4.iloc[0]['AsofTime']
                xMarketStatus = df_mw4.iloc[0]['MarketStatus']

        except:
            xPrice = 0
            xPrevClose = 0
            xOpen = 0
            xChange = 0
            xChangePerc = 0
            xFiftyTwoWeekRange = 0
            xDividend = '-'
            xTrailingPE = 0
            xTrailingEps = 0
            xMarketCap = 0

        if rowNo == '1':
            if float(xPrice) > float(xPrevClose):
                xColor = 'green'
            else : 
                xColor = 'red'

            # ------  Current Price Row 1 and Change Percentage Row 2
            row = \
            f"""<div> 
                    <span style='float: left; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{"Current Price: "}</b></span>
                    <span style='float: right; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:18px'><b>{xPrice}</b></span>
                </div>
            """
            st.markdown(row, unsafe_allow_html=True)
            row = \
                f"""<div> 
                        <span style='float: right; color: {xColor}; margin-top: 0; margin-bottom: 0; line-height: 2px; font-size:14px'><b>{xChange} ({xChangePerc}%)</b></span>
                    </div>
                """
            st.markdown(row, unsafe_allow_html=True)
            
            st.markdown('\n')

            # ------  After Hours Price Row 1 and Change Percentage Row 2
            if len(df_mw4) > 0:
                if xMarketStatus != 'Open':
                    xAfterMarketPrice = xAfterMarketPrice.replace("$", "")
                    xAfterMarketPrice = xAfterMarketPrice.replace(",", "")
                    xAfterMarketPrice = xAfterMarketPrice.strip()
                    if '-' in xAfterMarketChange:
                        xAftHrsColor = 'red'
                    else : 
                        xAftHrsColor = 'green'
                    row = \
                    f"""<div> 
                            <span style='float: left; margin-top: 0; margin-bottom: 0; line-height: 0px; font-size:12px'><b>{xMarketStatus}:</b></span>
                            <span style='float: right; margin-top: 0; margin-bottom: 0; line-height: 0px; font-size:12px'><b>{xAfterMarketPrice}</b></span>
                        </div>
                    """
                    st.markdown(row, unsafe_allow_html=True)
                    row = \
                        f"""<div> 
                                <span style='float: right; color: {xAftHrsColor}; margin-top: 0; margin-bottom: 0; line-height: 0px; font-size:12px'><b>{xAfterMarketChange} ({xAfterMarketPerc}%)</b></span>
                            </div>
                        """
                    st.markdown(row, unsafe_allow_html=True)
                    row = \
                        f"""<div> 
                                <span style='float: right; margin-top: 0; margin-bottom: 0; line-height: 0px; font-size:10px'>As of: {xAfterMarketTime}</span>
                            </div>
                        """
                    st.markdown(row, unsafe_allow_html=True)
                    st.markdown('\n')
        else:        

            # ------  Additional Stock Info Multi-Rows
            info_names = ["Previous Close: ", "Open: ", "52-Week Range: ", "Volume: ", \
                        "Dividend Rate & Yield: ", "Market Cap: ", "PE Ratio (TTM): ", "EPS (TTM): "]
            info_list = [xPrevClose, xOpen, xFiftyTwoWeekRange, xVolume, xDividend, \
                        xMarketCap, xTrailingPE, xTrailingEps]
            for name,infoValue in zip(info_names, info_list):
                row = \
                f"""<div> 
                        <span style='float: left;line-height: 5px; font-size:12px'><b>{name}</b></span>
                        <span style='float: right;line-height: 5px; font-size:12px'> {infoValue}</span>
                    </div>
                """
                st.markdown(row, unsafe_allow_html=True)





    #------ Function to DISPLAY SUMMARY (ETF) ----------
    def display_summary_etf(xList1):

        # Initilize to blanks
        xOpen, xDayRange, x52WeekRange, xMarketCap, xOutstanding, xAssets, xBeta, \
                xExpenseRatio, xTurnover, xYield, xDividend, xExDivDate, xAvgVolume = [""] * 13

        xTurnover = ''
        xOpen, xDayRange, x52WeekRange, xMarketCap, xOutstanding, xAssets, xBeta, \
                xExpenseRatio, xTurnover, xYield, xDividend, xExDivDate, xAvgVolume = xList1

        try:

            xTrailingPE = ''

            if 'regularMarketPrice' in ticker.info:
                if ticker.info['regularMarketPrice']:
                    xPrice = "%0.2f" % (ticker.info['regularMarketPrice'])              # force display two decimals

            if 'regularMarketPreviousClose' in ticker.info:
                if ticker.info['regularMarketPreviousClose']:
                    xPrevClose = "%0.2f" % (ticker.info['regularMarketPreviousClose'])               # force display two decimals

            if 'open' in ticker.info:
                if ticker.info['open']:
                    xOpen = "%0.2f" % (ticker.info['open'])                             # force display two decimals

            if xPrevClose != 0:
                xChange = "%0.2f" % (float(xPrice) - float(xPrevClose))

            if xPrevClose != 0:
                xChangePerc = "%0.2f" % ((float(xPrice) - float(xPrevClose)) / float(xPrevClose) * 100)

            if 'fiftyTwoWeekLow' not in ticker.info:
                xFiftyTwoWeekRange = x52WeekRange
            else:
                if ticker.info['fiftyTwoWeekLow'] and ticker.info and 'fiftyTwoWeekHigh':
                    xFiftyTwoWeekRange = str("%0.2f" % ticker.info['fiftyTwoWeekLow']) + ' - ' + str("%0.2f" % ticker.info['fiftyTwoWeekHigh'])
                else:
                    xFiftyTwoWeekRange = x52WeekRange

            xDayLowHigh = xDayRange
            if 'dayLow' in ticker.info and 'dayHigh' in ticker.info:
                if ticker.info['dayLow'] and ticker.info and 'dayHigh':
                    xDayLowHigh = str("%0.2f" % ticker.info['dayLow']) + ' - ' + str("%0.2f" % ticker.info['dayHigh'])

            xTotalAssets = xAssets
            if 'totalAssets' in ticker.info:
                if ticker.info['totalAssets']:
                    xTotalAssets = human_format(ticker.info['totalAssets'])

            if 'yield' in ticker.info:
                if ticker.info['yield']:
                    xYield = str(human_format(ticker.info['yield'] * 100)) + '%'
 
            if 'trailingPE' in ticker.info:
                if ticker.info['trailingPE']:
                    xTrailingPE = "%0.2f" % ticker.info['trailingPE']

        except:
            print ('Error in display_summary_etf')

        if float(xPrice) > float(xPrevClose):
            xColor = 'green'
        else : 
            xColor = 'red'

        row = \
        f"""<div> 
                <span style='float: left; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{"Today's Price: "}</b></span>
                <span style='float: right; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:18px'><b>{xPrice}</b></span>
            </div>
        """
        st.markdown(row, unsafe_allow_html=True)
                
        row = \
            f"""<div> 
                    <span style='float: right; color: {xColor}; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{xChange} ({xChangePerc}%)</b></span>
                </div>
            """
        st.markdown(row, unsafe_allow_html=True)
        
        st.markdown('\n')

        info_names = ["Previous Close: ", "Open: ", "Day Low-High", "52-Week Range: ",  \
                      "Yield: ", "ExpenseRatio: ", "Total Assets: ", "PE Ratio (TTM): ", "Turnover: "]
        info_list = [xPrevClose, xOpen, xDayLowHigh, xFiftyTwoWeekRange, \
                    xYield, xExpenseRatio, xTotalAssets, xTrailingPE, xTurnover]
        for name,infoValue in zip(info_names, info_list):
            row = \
            f"""<div> 
                    <span style='float: left;line-height: 10px; font-size:12px'><b>{name}</b></span>
                    <span style='float: right;line-height: 10px; font-size:12px'> {infoValue}</span>
                </div>
            """
            st.markdown(row, unsafe_allow_html=True)





    #------------------------ SETUP SIDEBAR TICKER INPUT -----------------------#
    with st.spinner('Loading Data...Please Wait...'):
        symbol = st.sidebar.text_input('Stock Symbol', value = 'AAPL') #search box

        ticker = yf.Ticker(symbol)

        if not symbol.isupper():
            symbol = symbol.upper()

        if not symbol: 
            st.sidebar.markdown('')
            st.sidebar.markdown("""<div style='text-align: center;'>Please search a ticker to see results.</div>""", unsafe_allow_html=True)


    #------------------------ SAVE TICKER TO GOOGLE SHEETS -----------------------#
    if st.sidebar.checkbox("Save Ticker"):

        with st.spinner('Loading Data...Please Wait...'):

            xError = '0'
            xPortfolio = st.sidebar.selectbox("Select Portfolio",
                                ['Watchlist', 'Dividends', 'ETFs', 'ToBuy', 'Analysts'])

            if is_prod:
                gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env variable
            else:    
                gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials

            sheet = gc.open('Research')
            wks = sheet.worksheet_by_title(xPortfolio)
            df1 = wks.get_as_df()

            if xPortfolio == 'Analysts':
                xAnalysts = df1['Source'].unique().tolist()
                xAnalysts.insert(0,'<New>')
                xAnalyst = st.sidebar.selectbox('Select Analyst:', xAnalysts)

                name = ''
                if xAnalyst == '<New>':
                    name = st.sidebar.text_input("Enter Analyst Name (required)")
                    xAnalyst = name
            
            if st.sidebar.button('Save'):

                if xPortfolio == 'Analysts':
                    if xAnalyst == '<New>' or len(xAnalyst) == 0:
                        if len(name) == 0:
                            xError = '1'
                            st.warning("Please fill out required field!")

                if xError != '1':
                    xDivExDate, xDivPayDate, xDivFreq = '', '', ''
                    if ticker.info['quoteType'] == 'EQUITY':
                        price = ticker.info['currentPrice']
                        xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = '', '', '', '', ''
                        if ticker.info['dividendRate']:
                            if ticker.info['dividendRate'] > 0:
                                xDivList = getData_MarketWatchDividends(symbol)  # GET DIV PAY DATE, ETC
                                xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = xDivList
                                # xDividendRate = ticker.info['dividendRate']
                                # xDividendYield = str("%0.2f" % (float(xDividendRate) / float(price) * 100))
                                # xDividend = str(xDividendRate) + ' (' + str(xDividendYield) + '%)'
                                xDividend = xDivAmount + ' (' + xDivYield + ')'
                        else:
                            xDividend = '-'
                    else:
                        price = ticker.info['regularMarketPrice']
                        xDividend = str(ticker.info['yield'] * 100) + '%'

                    # values = [[symbol,None,'xxx'],['aaa'],['bbb']]
                    # values = [[symbol,'=GOOGLEFINANCE(\"'+ symbol +'\","name")',str(date.today()),'1',price,None,dividends]]

                    if xPortfolio == 'Analysts':
                        values = [[symbol, None, xAnalyst, str(date.today()), '1', price, None, None, None, xDividend, xDivExDate, xDivPayDate, xDivFreq]]
                    else:
                        values = [[symbol, None, str(date.today()), '1', price, None, None, None, xDividend, xDivExDate, xDivPayDate, xDivFreq]]

                    wks.append_table(values, start='A2', end=None, dimension='ROWS', overwrite=True)  # Added

                    st.sidebar.write("Saved to: ", xPortfolio)


    st.sidebar.markdown('---')





    #---------------------------------------------------------------------
    #--------------------           TOP HEADER         -------------------
    #---------------------------------------------------------------------

    #---------------  Header Market Data  -------------------
    with st.spinner('Loading Data...Please Wait...'):
        df_mw1, df_mw2, df_mw3, df_mw4 = getData_MarketWatch(symbol)
        if len(df_mw1.index) > 0:
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([.5,1,1,1,1,1])
            #---------------  Dow  -------------------
            with col1:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Dow</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[0]['Value']
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size: 14px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[0]['Change'] + " (" + df_mw1.iloc[0]['Change %'] + " )"
                xColor = 'black'
                if '-' in df_mw1.iloc[0]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            #---------------  S&P 500  -------------------
            with col2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>S&P 500</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[1]['Value']
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size: 14px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[1]['Change'] + " (" + df_mw1.iloc[1]['Change %'] + " )"
                xColor = 'black'
                if '-' in df_mw1.iloc[1]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)

            #---------------  Nasdaq  -------------------
            with col3:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Nasdaq</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[2]['Value']
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size: 14px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw1.iloc[2]['Change'] + " (" + df_mw1.iloc[1]['Change %'] + " )"
                xColor = 'black'
                if '-' in df_mw1.iloc[2]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            #---------------  Gold  -------------------
            with col4:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Gold</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw2.iloc[0]['Value']
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size: 14px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw2.iloc[0]['Change'] + " (" + df_mw2.iloc[0]['Change %'] + " )"
                xColor = 'black'
                if '-' in df_mw2.iloc[0]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            #---------------  Oil  -------------------
            with col5:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Oil</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw2.iloc[1]['Value']
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size: 14px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)
                x1 = df_mw2.iloc[1]['Change'] + " (" + df_mw2.iloc[1]['Change %'] + " )"
                xColor = 'black'
                if '-' in df_mw2.iloc[1]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)

    st.write ('\n\n\n\n')

    # Main Page Header 
    st.markdown("""<div style='text-align: center;'><h3><b>THE STOCK ANALYSIS</b></h1></div>""", unsafe_allow_html=True)
    st.markdown("---")
    # st.markdown("")


    #---------------  Header (Equity) or (ETFs) Multi-Column Section  -------------------
    with st.spinner('Loading Data...Please Wait...'):
        if symbol and 'symbol' in ticker.info:

            summ = ''            
            if 'longBusinessSummary' in ticker.info:
                if ticker.info['longBusinessSummary']:
                    summ = ticker.info['longBusinessSummary']

            #---------------  Header (Equity) 3 Columns  -------------------
            if ticker.info['quoteType'] == 'EQUITY':
 
                hdr1a,hdr1b,hdr1c = st.beta_columns([0.5,3.5,2])
                with hdr1a:
                    if ticker.info['logo_url']:
                        st.image(ticker.info['logo_url'])
                with hdr1b: 
                    try:
                        st.subheader(ticker.info['longName'])
                        xIndustry = ticker.info['sector'] + " - " + ticker.info['industry']
                        row = f'<p style="font-family:sans-serif; float: left;line-height: 16px; font-size: 14px;">{xIndustry}</p>'
                        st.markdown(row, unsafe_allow_html=True)
                    except:
                        pass
                with hdr1c:
                    display_summary_equity(symbol,'1')

                hdr2a,hdr2b, hdr2c = st.beta_columns([4,0.25,2.1])
                with hdr2a:
                    with st.beta_expander(f'Description: {summ[0:250]} ... Read more'):
                        st.markdown(f'<p class="small-font"> {summ} !!</p>', unsafe_allow_html=True)
                with hdr2c: 
                    display_summary_equity(symbol,'2')

            else:
                #---------------  Header (ETFs) 2 Columns  -------------------
                xExpenseRatio = ''
                xList1 = []
                xList2 = []
                xList1, xList2 = getData_MarketWatchETFs(symbol)

                hdr1,hdr2, hdr3, hdr4 = st.beta_columns([4,2,1,2])
                with hdr1: 
                    try:
                        st.subheader(ticker.info['longName'])
                        xText = ticker.info['category']
                        row = f'<p style="font-family:sans-serif; float: left;line-height: 16px; font-size: 16px;">Category: {xText}</p>'
                        st.markdown(row, unsafe_allow_html=True)
                    except:
                        pass
                with hdr2: 
                        st.text ('\n')
                        st.text ('\n')
                        st.text ('\n')
                        st.text ('\n')
                        row = f'<p style="font-family:sans-serif; float: left;line-height: 12px; font-size: 14px;">YTD LIPPER RANKING</p>'
                        st.markdown(row, unsafe_allow_html=True)
                        info_names = ["Total Returns: ", "Consistent Return: ", "Preservation: ", \
                                      "Tax Efficiency: ", "Expense: "]
                        info_list = [xList2[0], xList2[1], xList2[2], xList2[3], xList2[4]]
                        for name, infoValue in zip(info_names, info_list):
                            row = \
                            f"""<div> 
                                    <span style='float: left;line-height: 10px; font-size:12px'><b>{name}</b></span>
                                    <span style='float: right;line-height: 10px; font-size:12px'>{infoValue}</span>
                                </div>
                            """
                            st.markdown(row, unsafe_allow_html=True)
                with hdr4:
                    display_summary_etf(xList1)

        else:
            st.write ('Invalid Ticker!')


    st.write ('\n\n')



    #---------------  LOAD YFINANCE DATA FOR 'SPY'  -------------------
    spy = yf.Ticker('SPY')
    spy_df = spy.history(period = '1y',interval='1d')
    spy_df.reset_index(inplace = True)
    # Get Percentage Return 
    r = [0]
    for i in range(1,len(spy_df)):
        val = (spy_df.Close[i] - spy_df.Close[0]) / spy_df.Close[0] *100
        r.append(val)
    spy_df['Return'] = r 


    #---------------  LOAD YFINANCE DATA FOR TICKER VARIABLE  -------------------
    df = ticker.history(period = '1y',interval='1d')
    df.reset_index(inplace=True)
    # Percentage return for Ticker 
    r = [0]
    for i in range(1,len(df)):
        val = (df.Close[i] - df.Close[0]) / df.Close[0] *100
        r.append(val)
    df['Return'] = r 


    new_df = pd.DataFrame(columns=['Date', 'SPY Return', f'{symbol} Return'])
    new_df['Date'] = spy_df.Date
    new_df['SPY Return'] = spy_df.Return
    new_df[f'{symbol} Return'] = df.Return



    #---------------  Overview Selection  -------------------
    if st.sidebar.checkbox("Overview", value = True):
        if symbol and 'symbol' in ticker.info:

            try:
                #--------  Display Stock Price Graph ----------------- 
                start = "2021-01-01" # start of graphics                   #
                today = date.today()+ datetime.timedelta(days=1)
                d1 = today.strftime("%Y-%m-%d")
                current_year, current_month, current_day = today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")
                tickerData = yf.download(symbol, start=start, end="{}".format(d1))
                tickerData['Date']=tickerData.index
                df1 = tickerData

                xRange = st.sidebar.slider('Select Range (days)', min_value=2,max_value=126, value=30)
            
                vert = '#599673'
                rouge = '#e95142'

                fig = make_subplots(rows=1, cols=2,
                                    specs=[[{'type': 'xy'},{'type':'indicator'}] for i in range (1)],
                                    column_widths=[0.85, 0.15],
                                    shared_xaxes=True,
                                    subplot_titles=[symbol, ''])

                def xColor(df):
                    if df1['Close'].iloc[-1*xRange]-df1['Close'].iloc[-1] < 0 :
                        return vert
                    else : return rouge

                fig.add_trace(go.Scatter(
                    y = df1['Close'],
                    x = df1['Date'],
                    line=dict(color=xColor(df1), width=1),
                    name="",
                    hovertemplate=
                    "Date: %{x}<br>" +
                    "Close: %{y}<br>"+
                    "Volume: %{text}<br>",
                    text = df1.Volume,
                ), row=1, col=1)

                fig.add_hline(y=df1['Close'].iloc[0],
                            line_dash="dot",
                            annotation_text="{}".format(df1['Date'][0].date()),
                            annotation_position="bottom left",
                            line_width=2, line=dict(color='black'),
                            annotation=dict(font_size=10),
                            row=1, col=1)

                fig.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = round(df1['Close'].iloc[-1],4),
                    number={'prefix': "$", 'font_size' : 40},
                    delta = {"reference": df1['Close'].iloc[-1*xRange], "valueformat": ".6f", "position" : "bottom", "relative":False},
                    title = {"text": symbol+" Last {}-days".format(xRange)},
                    domain = {'y': [0.5, 0.7], 'x': [0.55, 0.75]}),
                row=1, col=2)

                if xRange > 1 :
                    fig.add_shape(type="rect",
                                xref="x", yref="y",
                                x0=df1['Date'].iloc[-1*xRange].date().strftime('%Y-%m-%d'), y0=df1['Close'].min(),
                                x1=d1, y1=df1['Close'].max(),
                                fillcolor=xColor(df1),
                                row=1, col=1
                                )

                fig.update_layout(
                    template='simple_white',
                    showlegend=False,
                    font=dict(size=10),
                    autosize=False,
                    width=1400, height=300,
                    margin=dict(l=40, r=500, b=40, t=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_showticklabels=True,
                )

                st.subheader('Share price of last '+str(xRange)+' days\n')
                st.plotly_chart(fig)
                st.write ('\n\n\n')


                #--------  Display Return vs SP500 ----------------- 
                st.subheader('Percent Return vs SP500')
                per_return = px.line(new_df, x='Date', y=new_df.columns)
                per_return.update_layout(autosize=True,width=1000)
                st.write(per_return)

            except:
                pass



    #---------------  Technicals Selection  -------------------
    if st.sidebar.checkbox("Technicals", value = True):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol and 'symbol' in ticker.info:

                #--------  Display Price/MA, MACD and RSI ----------------- 
                df = ticker.history(period="1y")
                df1 = df
                df1['200 MA'] = df['Close'].rolling(200).mean()
                df1['50 MA'] = df['Close'].rolling(50).mean()
                df['exp1'] = df['Close'].ewm(span=12, adjust=False).mean()
                df['exp2'] = df['Close'].ewm(span=26, adjust=False).mean()
                df['macd'] = df['exp1']-df['exp2']
                df['exp3'] = df['macd'].ewm(span=9, adjust=False).mean()
                
                previous_15 = df['exp3'].shift(1)
                previous_45 = df['macd'].shift(1)
                Golden = df[((df['exp3'] <= df['macd']) & (previous_15 >= previous_45))]#.shift(1)
                #Golden['Average'] = (Golden['macd'] + Golden['exp3'])/2
                Death = df[((df['exp3'] >= df['macd']) & (previous_15 <= previous_45))]#.shift(1)
                
                rsi_period = 14
                chg = df['Close'].diff(1)
                gain = chg.mask(chg<0,0)
                loss = chg.mask(chg>0,0)
                avg_gain = gain.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()
                avg_loss = loss.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()
                rs = abs(avg_gain/avg_loss)
                rsi = 100-(100/(1+rs))
                df['RSI'] = rsi
                
                fig2 = go.Figure()
                fig2.add_trace(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name = 'CandleStick'))
                fig2.update_layout(autosize=True,width=1000,yaxis_title='Price'.format(symbol),xaxis_title='Dates'.format(symbol))
                fig2.add_trace(go.Scatter(x = df.index,y = df1['200 MA'],mode='lines', name='200MA')) #200 EMA
                fig2.add_trace(go.Scatter(x = df.index,y = df1['50 MA'],mode='lines', name='50MA')) #50 EMA
                fig2.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), #hide weekends
                            dict(values=["2020-12-25", "2021-01-01"])])  # hide Christmas and New Year's]
                
                df = df[-100:]
                Golden = df[((df['exp3'] <= df['macd']) & (previous_15 >= previous_45))]#.shift(1)
                Death = df[((df['exp3'] >= df['macd']) & (previous_15 <= previous_45))]#.shift(1)
                
                fig = go.Figure()
                #fig.add_trace(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name = 'CandleStick')) #CandleStick
                fig.add_trace(go.Scatter(y = df['macd'], x = df.index,marker_color='red',name='Selling'))
                fig.add_trace(go.Scatter(y = df['exp3'], x = df.index,marker_color='green',name='Buying'))
                fig.add_trace(go.Scatter(x = Golden.index,y = Golden['macd'],mode='markers',marker_line_width=2, marker_size=10,name='Golden'))
                fig.add_trace(go.Scatter(x = Death.index,y = (Death['exp3']),mode='markers',marker_line_width=2, marker_size=10,name='Death'))
                fig.update_layout(autosize=False,width=1000)
                
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(x = df.index,y = df['Volume']))
                fig3.update_layout(autosize=True,width=1000,yaxis_title='Volume'.format(symbol),xaxis_title='Dates')
                fig3.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), #hide weekends
                            dict(values=["2020-12-25", "2021-01-01"])])

                fig4 = go.Figure()
                fig4.update_layout(autosize=True,width=1000)
                fig4.add_trace(go.Scatter(y = df['RSI'], x = df.index,mode='lines', name='RSI'))
                #fig.add_trace(go.Scatter(y = 30, x = df.index,mode='lines'))
                fig4.add_shape(
                        type="line",
                        x0 = df.index[0],x1 = df.index[-1],
                        y0=30,y1=30,
                        line=dict(color='red', width=4,dash='dash'))
                fig4.add_shape(
                        type="line",
                        x0 = df.index[0],x1 = df.index[-1],
                        y0=70,y1=70,
                        line=dict(color='red', width=4,dash='dash'))
                
                st.subheader('12 Months Daily Chart: ')
                st.plotly_chart(fig2) #use_container_width = True)
                st.subheader('Volume')
                st.plotly_chart(fig3)
                st.subheader('MACD')
                st.plotly_chart(fig)
                st.subheader('RSI')
                st.plotly_chart(fig4)


                #---------------  Bollinger Bands  -------------------
                tickerDf = ticker.history(period='1y') #get the historical prices for this ticker

                st.subheader('**Bollinger Bands**')
                st.write ('\n\n')
                qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
                qf.add_bollinger_bands()
                fig = qf.iplot(asFigure=True)
                fig.update_layout(autosize=True,width=1000)
                st.plotly_chart(fig)



    #---------------  Fundamentals Selection  -------------------


    if st.sidebar.checkbox("Fundamentals", value = True):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol and 'symbol' in ticker.info:

                st.header(f'{symbol.upper()} Fundamentals')

                xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = '', '', '', '', ''
                if ticker.info['dividendRate']:
                    if ticker.info['dividendRate'] > 0:
                        xDivList = getData_MarketWatchDividends(symbol)  # GET DIV PAY DATE, ETC
                        xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = xDivList


                #---------------  Fundamentals (Equity) 2 Columns  -------------------
                if ticker.info['quoteType'] == 'EQUITY':

                    choice = st.sidebar.selectbox('Quarterly or Yearly Financials',['Yearly','Quarterly'])

                    buffer, left, right = st.beta_columns([0.5,2,2])
                    with left: 
                        if 'marketCap' in ticker.info:
                            if ticker.info['marketCap']:
                                num = human_format(ticker.info['marketCap'])
                                st.write('Market Cap: ', num) 
                        if 'trailingPE' in ticker.info:
                            if ticker.info['trailingPE']:
                                st.write('Trailing P/E: ', "%0.2f" % ticker.info['trailingPE'])
                        if 'forwardPE' in ticker.info:
                            if ticker.info['forwardPE']:
                                st.write('Forward P/E: ',   "%0.2f" % ticker.info['forwardPE'])
                        if 'bookValue' in ticker.info:
                            if ticker.info['bookValue']:
                                st.write('Book Value:   ', "%0.2f" % ticker.info['bookValue'])
                        if 'beta' in ticker.info:
                            if ticker.info['beta']:
                                st.write('Beta:   ', "%0.2f" % ticker.info['beta'])
                        if 'priceToBook' in ticker.info:
                            if ticker.info['priceToBook']:
                                st.write('Price to Book: ', "%0.2f" % ticker.info['priceToBook'])
                        if xDivAmount:
                                st.write('Dividend Amount:   ', xDivAmount)
                        if xDivYield:
                                st.write('Dividend Yield:   ', xDivYield)
                        if 'payoutRatio' in ticker.info:
                                if ticker.info['payoutRatio']:
                                    st.write('Payout Ratio:   ', "%0.2f" % ticker.info['payoutRatio'])
                    with right: 
                        if 'priceToSalesTrailing12Months' in ticker.info:
                            if ticker.info['priceToSalesTrailing12Months']:
                                st.write('Price to Sales: ',"%0.2f" % ticker.info['priceToSalesTrailing12Months'])
                        if 'trailingEps' in ticker.info:
                            if ticker.info['trailingEps']:
                                st.write('Trailing EPS:   ', "%0.2f" % ticker.info['trailingEps'])
                        if 'forwardEps' in ticker.info:
                            if ticker.info['forwardEps']:
                                st.write('Forward EPS: ',   "%0.2f" % ticker.info['forwardEps'])
                        if 'fiftyDayAverage' in ticker.info:
                            if ticker.info['fiftyDayAverage']:
                                st.write('50 Day Average: ', "%0.2f" % ticker.info['fiftyDayAverage'])
                        if 'twoHundredDayAverage' in ticker.info:
                            if ticker.info['twoHundredDayAverage']:
                                st.write('200 Day Average: ', "%0.2f" % ticker.info['twoHundredDayAverage'])
                        if 'pegRatio' in ticker.info:
                            if ticker.info['pegRatio']:
                                st.write('Peg Ratio: ', "%0.2f" % ticker.info['pegRatio'])
                        if xDivExDate:
                                st.write('Dividend Ex-Date:   ', xDivExDate)
                        if xDivPayDate:
                                st.write('Dividend Pay Date:   ', xDivPayDate)
                        if xDivFreq:
                                st.write('Dividend Frequency:   ', xDivFreq)
                    try: 
                        if choice == 'Yearly':
                            y_earning_df = ticker.earnings.reset_index()
                            y_rev = px.bar(data_frame=y_earning_df, x=y_earning_df.Year,y=y_earning_df.Revenue)
                            y_earning = px.bar(data_frame=y_earning_df, x=y_earning_df.Year,y=y_earning_df.Earnings)
                            st.write(y_earning)
                            st.write(y_rev)
                        if choice == 'Quarterly':
                            q_earning_df = ticker.quarterly_earnings.reset_index()
                            rev = px.bar(data_frame = q_earning_df, x=q_earning_df.Quarter, y=q_earning_df.Revenue)
                            earning = px.bar(data_frame = q_earning_df, x=q_earning_df.Quarter, y=q_earning_df.Earnings)
                            st.write(earning)
                            st.write(rev)
                    except:
                        st.write('No Data')

                else:
                    #---------------  Fundamentals (ETFs) 2 Columns  -------------------
                    buffer, left, right = st.beta_columns([0.5,2,2])
                    with left: 
                        if 'fundFamily' in ticker.info:
                            if ticker.info['fundFamily']:
                                st.write('Fund Family: ', ticker.info['fundFamily']) 
                        if 'trailingPE' in ticker.info:
                            if ticker.info['trailingPE']:
                                st.write('Trailing P/E: ', "%0.2f" % ticker.info['trailingPE'])
                        if 'beta' in ticker.info:
                            if ticker.info['beta']:
                                st.write('Beta:   ', "%0.2f" % ticker.info['beta'])
                        if ticker.info['regularMarketVolume']:
                            num = human_format(ticker.info['regularMarketVolume'])
                            st.write('Volume: ', num) 
                        # if ticker.info['averageVolume10days']:
                        #     num = human_format(ticker.info['averageVolume10days'])
                        #     st.write('Average Volume: ', num) 
                        if 'trailingAnnualDividendRate' in ticker.info:
                            if ticker.info['trailingAnnualDividendRate']:
                                st.write('Trailing Annual Dividend Rate: ',   "%0.2f" % ticker.info['trailingAnnualDividendRate'])
                        if 'trailingAnnualDividendYield' in ticker.info:
                            if ticker.info['trailingAnnualDividendYield']:
                                st.write('Trailing Annual Dividend Yield: ', "%0.2f" % ticker.info['trailingAnnualDividendYield'])
                    with right: 
                        if 'fiftyDayAverage' in ticker.info:
                            if ticker.info['fiftyDayAverage']:
                                st.write('50 Day Average: ', "%0.2f" % ticker.info['fiftyDayAverage'])
                        if 'twoHundredDayAverage' in ticker.info:
                            if ticker.info['twoHundredDayAverage']:
                                st.write('200 Day Average: ', "%0.2f" % ticker.info['twoHundredDayAverage'])
                        if 'threeYearAverageReturn' in ticker.info:
                            if ticker.info['threeYearAverageReturn']:
                                st.write('3-Year Average Return: ',"%0.2f" % ticker.info['threeYearAverageReturn'])
                        if 'fiveYearAverageReturn' in ticker.info:
                            if ticker.info['fiveYearAverageReturn']:
                                st.write('5-Year Average Return: ',   "%0.2f" % ticker.info['fiveYearAverageReturn'])


        st.write ('\n')
        st.write ('\n')




    #---------------  Analyst Recommendations  -------------------
    if st.sidebar.checkbox("Analyst Ratings"):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol and 'symbol' in ticker.info:

                try:
                    if type(ticker.recommendations) != type(None):
                        recs = ticker.recommendations.tail(3)
                        new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">Yahoo Finance</p>'
                        st.markdown(new_title, unsafe_allow_html=True)
                        recs.drop(recs.columns[[2, 3]], axis = 1, inplace = True)   # Drop Columns
                        recs.reset_index(inplace=True)                              # Remove Index Column
                        recs['Date'] = recs['Date'].dt.date                         # Set Date Column as index
                        recs = recs.sort_index(ascending=False)                     # Sort df index ascending
                        # st.table(recs.assign(hack='').set_index('hack'))            # Suppress showing index column

                        col2 = recs['Date']
                        col3 = recs['Firm']
                        col4 = recs['To Grade']
                        #the buffer = col1 and we never put anything in it
                        buffer, col2, col3, col4 = st.beta_columns([1,2,2,2])
                        col1a = str(recs['Date'][2])
                        col1b = str(recs['Date'][1])
                        col1c = str(recs['Date'][0])
                        col2a = str(recs['Firm'][2])
                        col2b = str(recs['Firm'][1])
                        col2c = str(recs['Firm'][0])
                        col3a = str(recs['To Grade'][2])
                        col3b = str(recs['To Grade'][1])
                        col3c = str(recs['To Grade'][0])
                        with col2:
                            # st.markdown(f'<p style="color: red; margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col1a}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col1a}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col1b}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col1c}</p>', unsafe_allow_html=True)
                        with col3:
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col2a}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col2b}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col2c}</p>', unsafe_allow_html=True)
                        with col4:
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col3a}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col3b}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p style="margin-top: 10; margin-bottom: 10;line-height: 8px; font-size:14px"> {col3c}</p>', unsafe_allow_html=True)

                    st.write ('\n\n')

                except:
                    st.write ('Error: Analyst Ratings (101)')
                    pass

                #---------------  Get Zacks Data  -------------------
                df1 = getData_Zacks(symbol)
                if len(df1.index) > 0:
                    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">Zacks.com</p>'
                    st.markdown(new_title, unsafe_allow_html=True)
                    st.table(df1.assign(hack='').set_index('hack'))

        
                #---------------  Get DiviData Data  -------------------
                df1 = getData_Dividata(symbol)
                if len(df1.index) > 0:
                    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">Dividata.com</p>'
                    st.markdown(new_title, unsafe_allow_html=True)
                    st.table(df1.assign(hack='').set_index('hack'))


                #---------------  Get TipRanks Data  -------------------
                df1 = getData_Tipranks(symbol)
                if len(df1.index) > 0:
                    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">Tipranks.com</p>'
                    st.markdown(new_title, unsafe_allow_html=True)
                    st.table(df1.assign(hack='').set_index('hack'))



                #---------------  Get Stockinvest.us Data  -------------------
                df1 = getData_StockInvest(symbol)
                if len(df1.index) > 0:
                    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">Stockinvest.us</p>'
                    st.markdown(new_title, unsafe_allow_html=True)
                    st.table(df1.assign(hack='').set_index('hack'))



                #---------------  MarketWatch.com Data  -------------------
                if len(df_mw3.index) > 0:
                    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">MarketWatch.com</p>'
                    st.markdown(new_title, unsafe_allow_html=True)
                    st.table(df_mw3.assign(hack='').set_index('hack'))



    if st.sidebar.checkbox("Add'l Sources"):
        if symbol and 'symbol' in ticker.info:

            st.markdown('---')
            row = '<p style="font-family:sans-serif; line-height: 14px; font-size: 16px;"><b>Research Ticker on any resources listed below:</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            st.markdown('\n')

            #-----------------------  LINE 1  ------------------------------------
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1,1])
            with col1:
                link = f'[Yahoo Finance](https://finance.yahoo.com/quote/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col2:
                link = f'[Zacks](https://www.zacks.com/stock/quote/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col3:
                link = f'[StockRSI](https://www.stockrsi.com/{symbol.lower()}/)'
                st.markdown(link, unsafe_allow_html=True)
            with col4:
                link = f'[Dividend Channel](https://www.dividendchannel.com/history/?symbol={symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col5:
                link = f'[Morningstar Stocks](https://www.morningstar.com/stocks/xnas/{symbol}/quote)'
                st.markdown(link, unsafe_allow_html=True)


            #-----------------------  LINE 2  ------------------------------------
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1,1])
            with col1:
                link = f'[MarketWatch](https://www.marketbeat.com/stocks/NYSE/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col2:
                link = f'[TradersPro](https://www.traderspro.com/#/stockAnalysis/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col3:
                link = f'[TipRanks](https://www.tipranks.com/stocks/{symbol}/forecast)'
                st.markdown(link, unsafe_allow_html=True)
            with col4:
                link = f'[DiviData](https://dividata.com/stock/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col5:
                link = f'[Morningstar ETFs](https://www.morningstar.com/etfs/arcx/{symbol}/quote)'
                st.markdown(link, unsafe_allow_html=True)


            #-----------------------  LINE 3  ------------------------------------
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1,1])
            with col1:
                link = f'[StockTwits](https://stocktwits.com/symbol/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col2:
                link = f'[Finviz](https://finviz.com/quote.ashx?t={symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col3:
                link = f'[StockConsultant](https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol={symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col4:
                link = f'[ChartMill](https://www.chartmill.com/stock/quote/{symbol}/profile)'
                st.markdown(link, unsafe_allow_html=True)
            with col5:
                link = f'[Morningstar Funds](https://www.morningstar.com/funds/xnas/{symbol}/quote)'
                st.markdown(link, unsafe_allow_html=True)


            #-----------------------  LINE 4  ------------------------------------
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1,1])
            with col1:
                link = f'[ValueLine](https://research.valueline.com/research#list=recent&sec=company&sym={symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col2:
                link = f'[StockInvest](https://stockinvest.us/stock/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col3:
                link = f'[Barchart](https://www.barchart.com/stocks/quotes/{symbol}/overview)'
                st.markdown(link, unsafe_allow_html=True)
            with col4:
                link = f'[Financhill](https://financhill.com/stock-price-chart/{symbol}-technical-analysis)'
                st.markdown(link, unsafe_allow_html=True)
            with col5:
                link = f'[CNBC](https://www.cnbc.com/quotes/{symbol}/)'
                st.markdown(link, unsafe_allow_html=True)


            #-----------------------  LINE 5  ------------------------------------
            buffer, col1, col2, col3, col4, col5 = st.beta_columns([0.2,1,1,1,1,1])
            with col1:
                link = f'[GuruFocus](https://www.gurufocus.com/stock/{symbol}/summary)'
                st.markdown(link, unsafe_allow_html=True)
            with col2:
                link = f'[Bloomberg](https://www.bloomberg.com/search?query={symbol})'
                st.markdown(link, unsafe_allow_html=True)
            with col3:
                link = f'[SeekingAlpha](https://seekingalpha.com/symbol/{symbol})'
                st.markdown(link, unsafe_allow_html=True)
            # with col4:
            #     link = f'[Financhill](https://financhill.com/stock-price-chart/{symbol}-technical-analysis)'
            #     st.markdown(link, unsafe_allow_html=True)
            # with col5:
            #     link = f'[CNBC](https://www.cnbc.com/quotes/{symbol}/)'
            #     st.markdown(link, unsafe_allow_html=True)




            st.markdown('---')


    st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)




def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
