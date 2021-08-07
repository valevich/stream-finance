import streamlit as st
import pandas as pd
import os
import pygsheets
from pygsheets.datarange import DataRange
import plotly.graph_objects as go
from apps.stock_scrape1 import getData_MarketWatch


def app():

    is_prod = os.environ.get('IS_HEROKU', None)

    st.sidebar.markdown('---')

    def display_header():
        #---------------  Header Market Data  -------------------
        symbol = 'AAPL'
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
                if '-' in df_mw1.iloc[1]['Change']:
                    xColor = 'red'
                else:
                    xColor = 'green'
                row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 12px;"><b>{x1}</b></p>'
                st.markdown(row, unsafe_allow_html=True)

        st.write ('\n\n\n\n')
        st.markdown("---")



    # @st.cache(show_spinner=False)
    def load_gsheet(gsheet):

            if is_prod:
                gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env
            else:    
                gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials

            sheet = gc.open('Research')
            wks = sheet.worksheet_by_title(gsheet)
            df = wks.get_as_df()

            xLists = ['Watchlist','Dividends','ETFs','ToBuy']
            if gsheet in xLists:


            # if gsheet != 'AnalystsRankings' and != 'Portfolio':
                df.drop(
                    columns=["7_day_Change", "30_day_Change", "90_day_Change", "Out_Shares"]
                )
                for i in range(len(df)):
                    if '(' in df['Dividend_Yield'].values[i]:
                        xDividend_Yield = str(df.Dividend_Yield)
                        xDividend_Yield = xDividend_Yield[xDividend_Yield.find("(")+1:xDividend_Yield.find(")")]
                        df['Dividend_Yield'].values[i] = xDividend_Yield

            return df



    def display_gsheet(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            st.title(gsheet)
            df1 = load_gsheet(gsheet)

            # st.write(df1.columns)
            # buyDate = df1['Buy_Date'].unique()
            # buyDate_SELECTED = st.sidebar.multiselect('Select countries', buyDate)
            # mask_buyDate = df1['Buy_Date'].isin(buyDate_SELECTED)
            # df1 = df1[mask_buyDate]

            # st.write(df1.columns)
            # cols = st.sidebar.multiselect('select columns:', df1.columns)
            # st.write('You selected:', cols)
            # st.write(df1[cols])

            font_color = ['black'] * 6 + \
                [['red' if  boolv else 'green' for boolv in df1['Today_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Gain_Loss'].str.contains('-')],
                ['black']]

            fig = go.Figure(data=[go.Table(
                columnwidth=[1,3.5,1.3,0.7,1.3,1.3,1.1,1.1,1.2,1.9,1.9,0.7,1.3,1.3,1,1,1.1,1.1,1.1],
                header=dict(values=list(['Symbol', 'Name', 'Buy Date', 'Shares', 'Cost/Share', 
                                        'Today', 'Today %', 'Gain/Loss', 'Div Yield',
                                        'Div Ex-Date', 'Div Pay-Date', 'Div Freq', 
                                        '52-Week Low', '52-Week High', 'EPS', 'PE',
                                        'Mkt Cap', 'Volume']),
                            fill_color='paleturquoise',
                            font=dict(color='black', family='Arial, sans-serif', size=10),
                            align='center'),
                cells=dict(values=[df1.Ticker, df1.Company, df1.Buy_Date, df1.Shares,
                                df1.Cost, df1.Today, df1.Today_Perc, df1.Gain_Loss,
                                df1.Dividend_Yield, df1.Div_Ex_Date, df1.Div_Pay_Date, 
                                df1.Div_Freq, df1.Low_52_wk, df1.High_52_wk, df1.EPS,
                                df1.PE, df1.Mkt_Cap, df1.Volume, ],
                        fill_color='lavender',
                        font_color=font_color,
                        height=25,
                        font=dict(size=11),
                        align = ['left', 'left', 'center', 'center', 'right']
                    )
                )
            ])

            fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1200,height=800)
            st.write(fig)



    def display_analysts(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            if st.sidebar.checkbox("Show Analyst Rankings"):
                st.title('Analyst Rankings')
                df0 = load_gsheet('AnalystsRankings')

                font_color = ['black'] * 2 + \
                    [['red' if  boolv else 'green' for boolv in df0['Average_Return'].str.contains('-')],
                    ['black']]

                fig = go.Figure(data=[go.Table(
                    columnwidth=[4,1.5,1.5],
                    header=dict(values=list(['Analyst', 'Total Tickers', 'Average Return']),
                            fill_color='paleturquoise',
                            font=dict(color='black', family='Arial, sans-serif', size=10),
                            align=['left', 'right']),
                    cells=dict(values=[df0.Source, df0.Tickers, df0.Average_Return],
                            fill_color='lavender',
                            font_color=font_color,
                            height=25,
                            font=dict(size=11),
                            align=['left', 'right']
                        )
                    )
                ])
                fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=500,height=700)
                st.write(fig)


            df1 = load_gsheet(gsheet)
            st.title(gsheet)

            xAnalysts = df1['Source'].unique().tolist()
            xAnalysts.insert(0,'All')
            xAnalystsChoice = st.sidebar.selectbox('Select Analyst:', xAnalysts)
            if xAnalystsChoice != 'All':
                df1 = df1.loc[(df1['Source'] == xAnalystsChoice)]


            font_color = ['black'] * 6 + \
                [['red' if  boolv else 'green' for boolv in df1['Today_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Gain_Loss'].str.contains('-')],
                ['black']]

            fig = go.Figure(data=[go.Table(
                columnwidth=[1,3.5,3.5,1.3,0.7,1.3,1.3,1.1,1.1,1.2,1.9,1.9,0.7,1.3,1.3,1,1,1.1,1.1,1.1],
                header=dict(values=list(['Symbol', 'Name',  'Analyst', 'Buy Date', 'Shares', 'Cost/Share', 
                                        'Today', 'Today %', 'Gain/Loss', 'Div Yield',
                                        'Div Ex-Date', 'Div Pay-Date', 'Div Freq', 
                                        '52-Week Low', '52-Week High', 'EPS', 'PE',
                                        'Mkt Cap', 'Volume']),
                            fill_color='paleturquoise',
                            font=dict(color='black', family='Arial, sans-serif', size=10),
                            align='center'),
                cells=dict(values=[df1.Ticker, df1.Company, df1.Source, df1.Buy_Date, df1.Shares,
                                df1.Cost, df1.Today, df1.Today_Perc, df1.Gain_Loss,
                                df1.Dividend_Yield, df1.Div_Ex_Date, df1.Div_Pay_Date, 
                                df1.Div_Freq, df1.Low_52_wk, df1.High_52_wk, df1.EPS,
                                df1.PE, df1.Mkt_Cap, df1.Volume, ],
                        fill_color='lavender',
                        font_color=font_color,
                        height=25,
                        font=dict(size=11),
                        align = ['left', 'left', 'left', 'center', 'center', 'right']
                    )
                )
            ])
            fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1400,height=800)
            st.write(fig)



    def display_portfolio(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            df1 = load_gsheet(gsheet)
            st.title(gsheet)

            xAccount = df1['Account'].unique().tolist()
            xAccount.insert(0,'All')
            xAccountChoice = st.sidebar.selectbox('Select Account:', xAccount)
            if xAccountChoice != 'All':
                df1 = df1.loc[(df1['Account'] == xAccountChoice)]

            #------------   CALCULATE PORTFOLIO TOTALS  --------------
            xTotalValue = 0.00
            xTotalTodayPerc = 0.00
            xTotalTodayAvg = 0.00
            xTotalCost = 0.00
            xTotalGainLoss = 0.00
            xTotalGainLossPerc = 0.00

            for i in range(0, len(df1)):
                #------------   xTotalValue  --------------
                xTemp = ''                                     
                xTemp = xTemp + df1.iloc[i]['TotalValue']
                xTemp = xTemp.replace('$', '') 
                xTemp = xTemp.replace(',', '') 
                xTotalValue = xTotalValue + float(xTemp)
                #------------   xTotalTodayPerc  --------------
                if df1.iloc[i]['TodayPerc']:
                    xTemp = ''
                    xTemp = xTemp + df1.iloc[i]['TodayPerc']
                    xTemp = xTemp.replace('%', '') 
                    xTemp = xTemp.replace(',', '') 
                    xTotalTodayPerc = xTotalTodayPerc + float(xTemp)
                #------------   xTotalCost  --------------
                xTemp = ''                                     
                xTemp = xTemp + df1.iloc[i]['TotalCost']
                xTemp = xTemp.replace('$', '') 
                xTemp = xTemp.replace(',', '') 
                xTotalCost = xTotalCost + float(xTemp)
                #------------   xTotalGainLoss  --------------
                if df1.iloc[i]['GainLoss']:
                    xTemp = ''                                     
                    xTemp = xTemp + df1.iloc[i]['GainLoss']
                    xTemp = xTemp.replace('$', '') 
                    xTemp = xTemp.replace(',', '') 
                    xTotalGainLoss = xTotalGainLoss + float(xTemp)
                #------------   xTotalGainLossPerc  --------------
                if df1.iloc[i]['GainLossPerc']:
                    xTemp = ''
                    xTemp = xTemp + df1.iloc[i]['GainLossPerc']
                    xTemp = xTemp.replace('%', '') 
                    xTemp = xTemp.replace(',', '') 
                    xTotalGainLossPerc = xTotalGainLossPerc + float(xTemp)

            xTotalTodayAvg = str(round(xTotalTodayPerc / float(len(df1)), 2)) + '%'
            xTotalGainLossPercAvg = str(round(xTotalGainLossPerc / float(len(df1)), 2)) + '%'

            display_portfolio_totals(xTotalValue, xTotalTodayAvg, xTotalCost, xTotalGainLoss, xTotalGainLossPercAvg)

            xLayout = st.sidebar.radio("Select Layout", ('Summary','Detail')) 

            if xLayout == 'Summary':
                font_color = ['black'] * 6 + \
                    [['red' if  boolv else 'green' for boolv in df1['TodayPerc'].str.contains('-')],
                    ['black'], ['black'],
                    ['red' if  boolv else 'green' for boolv in df1['GainLoss'].str.contains('-')],
                    ['red' if  boolv else 'green' for boolv in df1['GainLossPerc'].str.contains('-')],
                    ['black']]

                fig = go.Figure(data=[go.Table(
                    columnwidth=[1.1,1,3.5,1,1.4,1.3,1.1,1.4,1.4,1.3,1.2,1.2],
                    header=dict(values=list(['Account', 'Symbol', 'Company',  'Shares', 'Cost/Share', 
                                    'Today', 'Today %', 'Total Value', 'Total Cost', 
                                    'Gain/Loss', 'Gain/Loss %', 'Div Yield']),
                            fill_color='paleturquoise',
                            font=dict(color='black', family='Arial, sans-serif', size=10),
                            align='center'),
                    cells=dict(values=[df1.Account, df1.Ticker, df1.Company, df1.Shares, df1.ShareCost,
                                    df1.Today, df1.TodayPerc, df1.TotalValue, df1.TotalCost, 
                                    df1.GainLoss, df1.GainLossPerc, df1.DivYield],
                            fill_color='lavender',
                            font_color=font_color,
                            height=25,
                            font=dict(size=11),
                            align = ['left', 'left', 'left', 'center', 'center', 'right']
                        )
                    )
                ])
                fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=900,height=800)
                st.write(fig)
            else:
                font_color = ['black'] * 9 + \
                    [['red' if  boolv else 'green' for boolv in df1['TodayPerc'].str.contains('-')],
                    ['black'], ['black'],
                    ['red' if  boolv else 'green' for boolv in df1['GainLoss'].str.contains('-')],
                    ['red' if  boolv else 'green' for boolv in df1['GainLossPerc'].str.contains('-')],
                    ['black']]

                fig = go.Figure(data=[go.Table(
                    columnwidth=[1.1,1,3.5,1.3,1,1.4,1.4,1.1,1.3,1.1,1.7,1.7,1.5,1.2,1.1,1,1.3,1.2,1.5,1.5,0.7],
                    header=dict(values=list(['Account', 'Symbol', 'Company',  'Buy Date', 'Shares', 'Cost/Share', 
                                    'Stop/Loss', 'Stop/Loss %', 'Today', 'Today %', 
                                    'Total Value', 'Total Cost', 'Gain/Loss', 'Gain/Loss %',
                                    'Dividend', 'Div Yield', 'Div Annual', 'Div Yield Cost', 
                                    'Div Ex-Date', 'Div Pay-Date', 'Div Freq']),
                            fill_color='paleturquoise',
                            font=dict(color='black', family='Arial, sans-serif', size=10),
                            align='center'),
                    cells=dict(values=[df1.Account, df1.Ticker, df1.Company, df1.BuyDate, df1.Shares, df1.ShareCost,
                                    df1.StopLoss, df1.StopLossPerc, df1.Today, df1.TodayPerc, 
                                    df1.TotalValue, df1.TotalCost, df1.GainLoss, df1.GainLossPerc,
                                    df1.Dividend, df1.DivYield, df1.DivAnnual, df1.DivYieldCost, 
                                    df1.ExDivDate, df1.DivPayDate, df1.DivFreq],
                            fill_color='lavender',
                            font_color=font_color,
                            height=25,
                            font=dict(size=11),
                            align = ['left', 'left', 'left', 'center', 'center', 'right']
                        )
                    )
                ])
                fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1450,height=800)
                st.write(fig)



    def display_portfolio_totals(xTotalValue, xTotalTodayAvg, xTotalCost, xTotalGainLoss, xTotalGainLossPercAvg):

        st.write ('\n')
        buf1, buf2, col1, col2, col3, col4, col5 = st.beta_columns([0.1,0.1,1,1,1,1,1])
        #---------------  Todays Change $  -------------------
        with col1:
            row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Today ($)</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            x1 = xTotalTodayAvg.replace('-', '')
            x1 = x1.replace('%', '')
            x1 = round(float(x1),2)
            x2 = round(float(xTotalValue),2)
            # x3 = round((x2 * float(x1) / 100),2)
            x3 = (x2 * float(x1) / 100)
            x3 = str('$' + "{:,.2f}".format(x3))
            if '-' in xTotalTodayAvg:
                xColor = 'red'
                x3 = '-' + str(x3)
            else:
                xColor = 'green'
                x3 = str(x3)
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{x3}</b></p>'
            st.markdown(row, unsafe_allow_html=True)
        #---------------  Todays Change %  -------------------
        with col2:
            row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Today (%)</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            if '-' in xTotalTodayAvg:
                xColor = 'red'
            else:
                xColor = 'green'
            xTotalTodayAvg = str(xTotalTodayAvg)
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{xTotalTodayAvg}</b></p>'
            st.markdown(row, unsafe_allow_html=True)
        #---------------  Tootal Value  -------------------
        with col3:
            row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Total Value</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            xVal = str("{:,.2f}".format(xTotalValue))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>${xVal}</b></p>'
            st.markdown(row, unsafe_allow_html=True)
        with col4:
            row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Gain/Loss ($)</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            xGainLoss = str('$' + "{:,.2f}".format(xTotalGainLoss))
            # xGainLoss = str(round(float(xTotalGainLoss),2))
            if '-' in str(xTotalGainLoss):
                xColor = 'red'
            else:
                xColor = 'green'
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{xGainLoss}</b></p>'
            st.markdown(row, unsafe_allow_html=True)
        with col5:
            row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Gain/Loss (%)</b></p>'
            st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            xGainLossPerc = str(xTotalGainLossPercAvg)
            if '-' in xTotalGainLossPercAvg:
                xColor = 'red'
            else:
                xColor = 'green'
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{xGainLossPerc}</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        st.write ('\n')
        st.write ('\n')
        # st.markdown("---")









    #------------------  MAIN  -----------------------------
    display_header()

    xSelection = st.sidebar.radio("Select your List", ('Watchlist','Dividends', 'ETFs', 'ToBuy', 'Analysts', 'Portfolio')) 

    if xSelection == 'Watchlist':
        display_gsheet (xSelection)
    elif xSelection == 'Dividends': 
        display_gsheet (xSelection)
    elif xSelection == 'ETFs': 
        display_gsheet (xSelection)
    elif xSelection == 'ToBuy': 
        display_gsheet (xSelection)
    elif xSelection == 'Analysts': 
        display_analysts (xSelection)
    elif xSelection == 'Portfolio': 
        display_portfolio (xSelection)













    #---------- Append
    # wks.clear()
    # values = [['aaa']]
    # wks.append_table(values, start='A1', end=None, dimension='ROWS', overwrite=True)  # Added

    ##---------- Get Column Names
    # all_values = wks.get_all_values()
    # cleaned_values = [[item for item in unique_list if item ]for unique_list in all_values]
    # st.write (cleaned_values[0])

    # #---------- Get 1st Column
    # first_column = wks.get_col(1)
    # first_column_data = first_column[1:] # We are doing a python slice here to avoid 
    #                                      # extracting the column names from the first row (keyword)
    # st.write (first_column_data)

    # #---------- Get every row
    # for row in wks:
    #     st.write (row)

    #---------- Replace all values
    # wks.replace("NaN", replacement="0")


    #---------- Update a single cell.
    # wks.update_value('B20', "Numbers on Stuff")

    #---------- Get last row
    # st.write (f"The last row is {wks.rows}")

    #---------- How To Bold Cells
    # model_cell = wks.cell('A1')
    # model_cell.set_text_format('bold', True)
    # DataRange('A1','F1', worksheet=wks).apply_format(model_cell)

    #---------- Export A Google Sheet To A .CSV
    # wks.export(filename='this_is_a_csv_file')

    #---------- Export A Google Sheet To Dataframe and then to JSON
    # st.write (wks.get_as_df().to_json())

    #---------- Export A Google Sheet To Dataframe











    # cells = wks.find("NaN", searchByRegex=False, matchCase=False, 
    #     matchEntireCell=False, includeFormulas=False, 
    #     cols=(3,6), rows=None, forceFetch=True)
    # wks.update_values(crange=None, values=None, cell_list=None, extend=False, majordim='ROWS', parse=None)
    # for cell in cells:
    #     cell.value = "Other"
    # wks.update_values(cell_list=cells)



    # # Read into dataframe
    # dataframe_two = wks.get_as_df()
    # dataframe_two.head(6)




    # news1, news2 = st.beta_columns([1,5])

    # with news1:
    #     st.image('https://cdn.pixabay.com/photo/2016/10/10/22/38/business-1730089_1280.jpg')

    # with news2: 
    #     st.markdown("***")









        # #---------------  gsheetsdb -------------
        # scope = ['https://spreadsheets.google.com/feeds',
        #         'https://www.googleapis.com/auth/drive']

        # credentials = service_account.Credentials.from_service_account_info(
        #     st.secrets["gcp_service_account"], scopes = scope)
        # client = Client(scope=scope, creds=credentials)
        # spreadsheetname = 'Research'
        # spread = Spread(spreadsheetname, client=client)

        # sh = client.open(spreadsheetname)
        # worksheet_list = sh.worksheets()

        # def worksheet_names():
        #     sheet_names = []
        #     for sheet in worksheet_list:
        #         sheet_names.append(sheet.title)
        #     return sheet_names

        # def load_the_spreadsheet(spreadsheetname):
        #     worksheet = sh.worksheet(spreadsheetname)
        #     df = DataFrame(worksheet.get_all_records())
        #     return df

        # def update_the_spreadsheet(spreadsheetname,dataframe):
        #     col = ['Date','Company']
        #     spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
        #     st.sidebar.info('Spreadsheet Updated')
            

        # #Load from Spreadsheet
        # what_sheets = worksheet_names()
        # ws_choice = st.radio('Available Worksheets', what_sheets)

        # #Create Select Box 
        # df = load_the_spreadsheet(ws_choice)

        # #Show Selection
        # select_CID = st.sidebar.selectbox('IPOs',list(df['Company'])) 


        # #Add Item to Spreadsheet
        # add = st.sidebar.checkbox('Add New Ticker')
        # if add:
        #     cid_entry = st.sidebar.text_input('New Ticker')
        #     confirm_input = st.sidebar.button('Confirm')

        #     if confirm_input:
        #         now = date.today()
        #         opt = {'IPOs': [cid_entry],
        #                 'Date': [now]}
        #         opt_df = DataFrame(opt)
        #         df = load_the_spreadsheet('IPOs')
        #         new_df = df.append(opt_df,ignore_index=True)
        #         update_the_spreadsheet('IPOs', new_df)
