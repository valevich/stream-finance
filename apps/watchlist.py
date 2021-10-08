import streamlit as st
import pandas as pd
import os
import pygsheets
from pygsheets.datarange import DataRange
import plotly.graph_objects as go
from apps.stock_scrape1 import getData_MarketWatch
from apps.stock_scrape1 import getData_MarketWatchDividends
from apps.stock_scrape2 import getData_stockinvest
import datetime
import yfinance as yf 
import time
from st_aggrid import AgGrid                                 
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def app():

    is_prod = os.environ.get('IS_HEROKU', None)

    st.sidebar.markdown('---')

    def display_header():
        #---------------  Header Market Data  -------------------
        symbol = 'AAPL'
        df_mw1, df_mw2, df_mw3, df_mw4 = getData_MarketWatch(symbol)
        if len(df_mw1.index) > 0:
            buffer, col1, col2, col3, col4, col5 = st.columns([.5,1,1,1,1,1])
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
        st.markdown("---")



    # @st.cache(show_spinner=False)
    def load_gsheet(gsheet):

            if is_prod:
                gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env
            else:    
                gc = pygsheets.authorize(service_file='client_secret.json') # using local account credentials

            sheet = gc.open('Research')
            wks = sheet.worksheet_by_title(gsheet)
            df = wks.get_as_df()

            return df



    def display_gsheet(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            st.title(gsheet)
            df1 = load_gsheet(gsheet)
            df1.drop(df1.columns[[3]], axis = 1, inplace = True)
            df1.rename(columns = {'Buy_Date':'Buy Date', 
                    'Today_Perc':'Today%',
                    'Gain_Loss':'Gain',
                    'Dividend_Yield':'Yield',
                    'Div_Ex_Date':'Ex-Date',
                    'Div_Pay_Date':'Pay Date',
                    'Div_Freq':'Freq'},
                        inplace=True)
            style_negative = JsCode(
                """
                function(params) {
                    if (params.value.includes('-')) {return {'color': 'red'}} 
                    else {return {'color': 'green'}}
                };
                """
            )
            gb = GridOptionsBuilder.from_dataframe(df1)
            gb.configure_default_column(groupable=True, 
                                            value=True, 
                                            enableRowGroup=True, 
                                            editable=True,
                                            enableRangeSelection=True,
                                        )
            gb.configure_column("Ticker", maxWidth=75)
            gb.configure_column("Company", maxWidth=200)
            gb.configure_column("Buy Date", maxWidth=100)
            gb.configure_column("Cost", maxWidth=85)
            gb.configure_column("Today", maxWidth=85)
            gb.configure_column("Today%", cellStyle=style_negative, maxWidth=88)
            gb.configure_column("Gain", cellStyle=style_negative, maxWidth=85)
            gb.configure_column("Yield", maxWidth=100)
            gb.configure_column("Ex-Date", maxWidth=100)
            gb.configure_column("Pay Date", maxWidth=100)
            gb.configure_column("Freq", maxWidth=80)
            gridOptions = gb.build()
            data = AgGrid(
                df1,
                gridOptions=gridOptions,
                height=850,
                width='100%',
                theme='light',     # valid themes: 'streamlit', 'light', 'dark', 'blue', 'fresh', 'material'
                # defaultWidth=25,
                # fit_columns_on_grid_load=True, 
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True
            )

            #------------   Using Plotly Tables - Replaced with Ag-Grid  --------------
            # st.title(gsheet)
            # df1 = load_gsheet(gsheet)
            # font_color = ['black'] * 6 + \
            #     [['red' if  boolv else 'green' for boolv in df1['Today_Perc'].str.contains('-')],
            #     ['red' if  boolv else 'green' for boolv in df1['Gain_Loss'].str.contains('-')],
            #     ['black']]
            # fig = go.Figure(data=[go.Table(
            #     columnwidth=[1,3.5,1.3,0.7,1.3,1.3,1.1,1.1,1.2,1.9,1.9,0.7,1.3,1.3,1,1,1.1,1.1,1.1],
            #     header=dict(values=list(['Symbol', 'Name', 'Buy Date', 'Shares', 'Cost/Share', 
            #                             'Today', 'Today %', 'Gain/Loss', 'Div Yield',
            #                             'Div Ex-Date', 'Div Pay-Date', 'Div Freq', 
            #                             '52-Week Low', '52-Week High', 'EPS', 'PE',
            #                             'Mkt Cap', 'Volume']),
            #                 fill_color='paleturquoise',
            #                 font=dict(color='black', family='Arial, sans-serif', size=10),
            #                 align='center'),
            #     cells=dict(values=[df1.Ticker, df1.Company, df1.Buy_Date, df1.Shares,
            #                     df1.Cost, df1.Today, df1.Today_Perc, df1.Gain_Loss,
            #                     df1.Dividend_Yield, df1.Div_Ex_Date, df1.Div_Pay_Date, 
            #                     df1.Div_Freq, df1.Low_52_wk, df1.High_52_wk, df1.EPS,
            #                     df1.PE, df1.Mkt_Cap, df1.Volume, ],
            #             fill_color='lavender',
            #             font_color=font_color,
            #             height=25,
            #             font=dict(size=11),
            #             align = ['left', 'left', 'center', 'center', 'right']
            #         )
            #     )
            # ])
            # fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1200,height=800)
            # st.write(fig)
            #--------------------------------------------------------------------------------------




    def display_analysts(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            if st.sidebar.checkbox("Show Analyst Rankings"):
                st.title('Analyst Rankings')
                df0 = load_gsheet('AnalystsRankings')

                style_AvgReturn = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('-')) {return {'backgroundColor': 'pink'}} 
                        else {return {'backgroundColor': 'lightgreen'}} 
                    };
                    """
                )
                gb = GridOptionsBuilder.from_dataframe(df0)
                gb.configure_default_column(groupable=True, 
                                                value=True, 
                                                enableRowGroup=True, 
                                                editable=True,
                                                enableRangeSelection=True,
                                            )
                gb.configure_column("Average_Return", cellStyle=style_AvgReturn)
                gridOptions = gb.build()
                data = AgGrid(
                    df0,
                    gridOptions=gridOptions,
                    height=850,
                    width='100%',
                    theme='light',     # valid themes: 'streamlit', 'light', 'dark', 'blue', 'fresh', 'material'
                    enable_enterprise_modules=True,
                    allow_unsafe_jscode=True
                )

            st.title(gsheet)
            df1 = load_gsheet(gsheet)
            df1.drop(df1.columns[[1, 4, 9, 10, 11, 12]], axis = 1, inplace = True)
            # xAnalysts = df1['Source'].unique().tolist()
            # xAnalysts.insert(0,'All')
            # xAnalystsChoice = st.sidebar.selectbox('Select Analyst:', xAnalysts)
            # if xAnalystsChoice != 'All':
            #     df1 = df1.loc[(df1['Source'] == xAnalystsChoice)]

            style_negative = JsCode(
                """
                function(params) {
                    if (params.value.includes('-')) {return {'color': 'red'}} 
                    else {return {'color': 'green'}}
                };
                """
            )
            style_AvgReturn = JsCode(
                """
                function(params) {
                    if (params.value.includes('-')) {return {'backgroundColor': 'pink'}} 
                    else {return {'backgroundColor': 'lightgreen'}} 
                };
                """
            )
            gb = GridOptionsBuilder.from_dataframe(df1)
            gb.configure_default_column(groupable=True, 
                                            value=True, 
                                            enableRowGroup=True, 
                                            editable=True,
                                            enableRangeSelection=True,
                                        )
            gb.configure_column("Today_Perc", cellStyle=style_negative)
            gb.configure_column("Gain_Loss", cellStyle=style_negative)
            gb.configure_column("AvgReturn", cellStyle=style_AvgReturn)
            gridOptions = gb.build()
            data = AgGrid(
                df1,
                gridOptions=gridOptions,
                height=1000,
                width='100%',
                theme='light',     # valid themes: 'streamlit', 'light', 'dark', 'blue', 'fresh', 'material'
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True
            )

            #------------       Using Plotly Tables - Replaced with Above Ag-Grid      --------------
            # font_color = ['black'] * 7 + \
            #     [['red' if  boolv else 'green' for boolv in df1['Today_Perc'].str.contains('-')],
            #     ['red' if  boolv else 'green' for boolv in df1['Gain_Loss'].str.contains('-')],
            #     ['black']]
            # fig = go.Figure(data=[go.Table(
            #     columnwidth=[1,3.5,3.5,1.3,0.7,1.3,1.3,1.1,1.1,1.2,1.9,1.9,0.7,1.3,1.3,1,1,1.1,1.1,1.1],
            #     header=dict(values=list(['Symbol', 'Name',  'Analyst', 'Buy Date', 'Shares', 'Cost/Share', 
            #                             'Today', 'Today %', 'Gain/Loss', 'Div Yield',
            #                             'Div Ex-Date', 'Div Pay-Date', 'Div Freq', 
            #                             '52-Week Low', '52-Week High', 'EPS', 'PE',
            #                             'Mkt Cap', 'Volume']),
            #                 fill_color='paleturquoise',
            #                 font=dict(color='black', family='Arial, sans-serif', size=10),
            #                 align='center'),
            #     cells=dict(values=[df1.Ticker, df1.Company, df1.Source, df1.Buy_Date, df1.Shares,
            #                     df1.Cost, df1.Today, df1.Today_Perc, df1.Gain_Loss,
            #                     df1.Dividend_Yield, df1.Div_Ex_Date, df1.Div_Pay_Date, 
            #                     df1.Div_Freq, df1.Low_52_wk, df1.High_52_wk, df1.EPS,
            #                     df1.PE, df1.Mkt_Cap, df1.Volume, ],
            #             fill_color='lavender',
            #             font_color=font_color,
            #             height=25,
            #             font=dict(size=11),
            #             align = ['left', 'left', 'left', 'center', 'center', 'right']
            #         )
            #     )
            # ])
            # fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1400,height=800)
            # st.write(fig)
            #--------------------------------------------------------------------------------------



    def display_portfolio(gsheet):
        with st.spinner('Loading Data...Please Wait...'):

            df1 = load_gsheet(gsheet)

            #------------   CALCULATE EACH ACCOUNT TOTALS  --------------
            xAccount = df1['Account'].unique().tolist()
            xAccount.sort()
            xAccount.insert(0,'All')
            xAccountChoice = st.sidebar.selectbox('Select Account:', xAccount)
            st.title('Portfolio: ' + xAccountChoice)
            st.write ('\n')

            if xAccountChoice != 'All':
                df1 = df1.loc[(df1['Account'] == xAccountChoice)]

            xTotalValue, xTotalTodayPerc, xTotalTodayAvg, xTotalToday, xTotalGainLoss, xTotalGainLossPerc = [0] * 6
            xGrandTotalValue, xGrandTotalTodayPerc, xGrandTotalTodayAvg, xGrandTotalToday, xGrandTotalGainLoss, xGrandTotalGainLossPerc = [0] * 6

            df2 = df1.copy()
            df2['TotalValue'] = df2['TotalValue'].str.replace('$','')
            df2['TotalValue'] = df2['TotalValue'].str.replace(',','')
            df2['GainLoss'] = df2['GainLoss'].str.replace('$','')
            df2['GainLoss'] = df2['GainLoss'].str.replace(',','')
            df2['GainLoss'] = pd.to_numeric(df2['GainLoss'], errors='coerce').astype('float')
            df2['TodayPerc'] = df2['TodayPerc'].str.replace('%','')
            df2['TodayPerc'] = df2['TodayPerc'].str.replace(',','')
            df2['TodayPerc'] = pd.to_numeric(df2['TodayPerc'], errors='coerce').astype('float')
            df2['GainLossPerc'] = df2['GainLossPerc'].str.replace('%','')
            df2['GainLossPerc'] = df2['GainLossPerc'].str.replace(',','')
            df2['GainLossPerc'] = pd.to_numeric(df2['GainLossPerc'], errors='coerce').astype('float')
            df2['TotalValue'] = df2.TotalValue.astype(float)
            df2['TodayPerc'] = df2.TodayPerc.astype(float)
            df2['GainLoss'] = df2.GainLoss.astype(float)
            df2['GainLossPerc'] = df2.GainLossPerc.astype(float)
            df2 = df2.groupby(['Account']).agg({'TotalValue': "sum", 'TodayPerc': 'mean', 'GainLoss': 'sum', 'GainLossPerc': 'mean'})

            xCntr = 0
            for i in range(0, len(df2)):
                df2['Account'] = df2.index
                xAccount = df2.iloc[i]['Account']
                xTotalValue = df2.iloc[i]['TotalValue']
                xTotalTodayPerc = df2.iloc[i]['TodayPerc']
                xTotalToday = (xTotalValue * xTotalTodayPerc / 100)
                xTotalGainLoss = df2.iloc[i]['GainLoss']
                xTotalGainLossPerc = df2.iloc[i]['GainLossPerc']
                xGrandTotalValue = xGrandTotalValue + xTotalValue
                xGrandTotalTodayPerc = xGrandTotalTodayPerc + xTotalTodayPerc
                xGrandTotalToday = xGrandTotalToday + xTotalToday
                xGrandTotalGainLoss = xGrandTotalGainLoss + xTotalGainLoss
                xGrandTotalGainLossPerc = xGrandTotalGainLossPerc + xTotalGainLossPerc
                xCntr = xCntr + 1
                display_portfolio_totals(xCntr, xAccount, xTotalValue, xTotalTodayPerc, xTotalToday, xTotalGainLoss, xTotalGainLossPerc)

            st.write ('\n')

            if xAccountChoice == 'All':
                row = '<hr style="height:1px;width:95%;border-width:0;color:gray;background-color:gray;margin-top: 0.1em;margin-bottom: 0.1em;">'
                st.markdown(row, unsafe_allow_html=True)
                xGrandTotalTodayPerc = xGrandTotalTodayPerc / len(df2)
                xGrandTotalGainLossPerc = xGrandTotalGainLossPerc / len(df2)
                display_portfolio_totals(xCntr, 'Total' ,xGrandTotalValue, xGrandTotalTodayPerc, xGrandTotalToday, xGrandTotalGainLoss, xGrandTotalGainLossPerc)


            st.write ('\n')
            st.write ('\n')
            st.write ('\n')


            xOption = st.sidebar.radio("Select Option", ('Summary','Detail','New Transaction','Held Stocks')) 

            #-------------------------  PORTFOLIO SUMMARY OR DETAIL VIEW --------------------------
            if xOption == 'Summary' or xOption == 'Detail':

                df1.rename(columns = {'BuyDate':'Date', 
                        'ShareCost':'Cost',
                        'StopLoss':'Stop',
                        'StopLossPerc':'Stop%',
                        'TodayPerc':'Today%',
                        'GainLoss':'Gain',
                        'TotalValue':'Value',
                        'GainLossPerc':'Gain%',
                        'DivYield':'Yield',
                        'Dividend':'DivRate',
                        'DivAnnual':'Annual',
                        'DivYieldCost':'YieldCost',
                        'ExDivDate':'Ex-Date',
                        'DivPayDate':'PayDate',
                        'DivFreq':'Freq'},
                            inplace=True)

                if xOption == 'Summary':
                    df1.drop(df1.columns[[3,6,14,16,17,18,19,20]], axis = 1, inplace = True)

                style_negative = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('-')) {return {'color': 'red'}} 
                        else {return {'color': 'green'}}
                    };
                    """
                )
                gb = GridOptionsBuilder.from_dataframe(df1)
                gb.configure_default_column(groupable=True, 
                                                value=True, 
                                                enableRowGroup=True, 
                                                editable=True,
                                                enableRangeSelection=True,
                                            )
                gb.configure_column("Account", maxWidth=80)
                gb.configure_column("Ticker", maxWidth=80)
                gb.configure_column("Company", maxWidth=200)
                gb.configure_column("Shares", maxWidth=81)
                gb.configure_column("Cost", maxWidth=85)
                gb.configure_column("Stop%", maxWidth=80)
                gb.configure_column("Today", maxWidth=85)
                gb.configure_column("Value", maxWidth=100)
                gb.configure_column("TotalCost", maxWidth=100)
                gb.configure_column("Today%", cellStyle=style_negative, maxWidth=88)
                gb.configure_column("Gain", cellStyle=style_negative, maxWidth=90)
                gb.configure_column("Gain%", cellStyle=style_negative, maxWidth=85)
                gb.configure_column("Yield", maxWidth=90)
                if xOption == 'Detail':
                    gb.configure_column("Date", maxWidth=85)
                    gb.configure_column("Stop", maxWidth=75)
                    gb.configure_column("DivRate", maxWidth=90)
                    gb.configure_column("YieldCost", maxWidth=97)
                    gb.configure_column("Annual", maxWidth=90)
                    gb.configure_column("Ex-Date", maxWidth=90)
                    gb.configure_column("PayDate", maxWidth=90)
                    gb.configure_column("Freq", maxWidth=70)
 
                gridOptions = gb.build()
                data = AgGrid(
                    df1,
                    gridOptions=gridOptions,
                    height=850,
                    width='100%',
                    theme='light',     # valid themes: 'streamlit', 'light', 'dark', 'blue', 'fresh', 'material'
                    # defaultWidth=25,
                    # fit_columns_on_grid_load=True, 
                    enable_enterprise_modules=True,
                    allow_unsafe_jscode=True
                )


            #-------------------------  NEW TRANSACTION  --------------------------
            elif xOption == 'New Transaction':

                #-------------- New Transaction Row 1 ----------------
                col1, col2, col3, col4, col5 = st.columns([1.5,1.5,1.5,1,4])
                with col1:
                    xAction = st.selectbox(
                        'Select Buy/Sell',
                        ('Buy', 'Sell', 'Dividend'))
                with col2:
                    if xAction == 'Sell' or xAction == 'Buy':
                        xAccount = df1['Account'].unique().tolist()
                        xAccount.sort()
                        xAccount.insert(0,'')
                        xAccountChoice = st.selectbox('Select Account:', xAccount)
                with col3:
                    if xAction == 'Sell':
                        if xAccountChoice != '':
                            df_tick = df1[df1['Ticker']!='CASH']
                            df_tick = df_tick.loc[(df_tick['Account'] == xAccountChoice)]
                            xTicker = df_tick['Ticker'].unique().tolist()
                            xAccount.sort()
                            xTicker.insert(0,'')
                            xTickerChoice = st.selectbox('Select Ticker:', xTicker)
                    elif xAction == 'Buy':
                        if xAccountChoice != '':
                            xTickerChoice = st.text_input('Ticker:').upper()

                with col5:
                    if xAction == 'Sell':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                st.write ('\n')
                                x1 = (df_tick[df_tick.Ticker == xTickerChoice].Company.item())
                                x2 = (df_tick[df_tick.Ticker == xTickerChoice].Today.item())
                                row = f'<p style="font-family:fantasy; margin-top: 0; margin-bottom: 0; color:Blue; font-size: 22px;"><b>{x1}</b></p>'
                                st.markdown(row, unsafe_allow_html=True)
                                row = f'<p style="font-family:verdana; margin-top: 0; margin-bottom: 0; color:Blue; font-size: 14px;">Current Price: {x2}</p>'
                                st.markdown(row, unsafe_allow_html=True)
                    elif xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                st.write ('\n')
                                ticker = yf.Ticker(xTickerChoice)
                                x1 = ticker.info['longName']
                                x2 = ticker.info['regularMarketPrice']
                                row = f'<p style="font-family:fantasy; margin-top: 0; margin-bottom: 0; color:Blue; font-size: 22px;"><b>{x1}</b></p>'
                                st.markdown(row, unsafe_allow_html=True)
                                row = f'<p style="font-family:verdana; margin-top: 0; margin-bottom: 0; color:Blue; font-size: 14px;">Current Price: {x2}</p>'
                                st.markdown(row, unsafe_allow_html=True)

                #-------------- New Transaction Row 2 ----------------
                st.write ('\n')
                col1, col2, col3, col4 = st.columns([2,3,3,3])
                with col1:
                    if xAction == 'Sell' or xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                xTransDate = st.date_input('Transaction Date')
                with col2:
                    if xAction == 'Sell' or xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                xTransPrice = st.number_input('Transaction Price', format="%.4f")
                with col3:
                    if xAction == 'Sell' or xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                xShares = st.number_input('Shares', format="%.4f")

                #-------------- New Transaction Row 3 ----------------
                st.write ('\n')
                col1, col2, col3 = st.columns([3,0.2,7.5])
                with col1:
                    if xAction == 'Sell':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                if xTransPrice > 0:
                                    if xShares > 0:
                                        if st.button ('Submit'):
                                            xPrevDate = (df_tick[df_tick.Ticker == xTickerChoice].BuyDate.item())
                                            xPrevShares = (df_tick[df_tick.Ticker == xTickerChoice].Shares.item())
                                            xPrevShareCost = (df_tick[df_tick.Ticker == xTickerChoice].ShareCost.item())
                                            xPrevTotalCost = (df_tick[df_tick.Ticker == xTickerChoice].TotalCost.item())
                                            process_transaction(xAction, xAccountChoice, xTickerChoice, xTransDate, xTransPrice, xShares, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost, '', '', '', '')
                                            print (df_tick[df_tick.Ticker == xTickerChoice].astype('str').values)
                    elif xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                if xTransPrice > 0:
                                    if xShares > 0:
                                        if st.button ('Submit'):
     
                                            if ticker.info['quoteType'] == 'EQUITY':
                                                price = ticker.info['currentPrice']
                                                xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = '', '', '', '', ''
                                                if ticker.info['dividendRate']:
                                                    if ticker.info['dividendRate'] > 0:
                                                        xDivList = getData_MarketWatchDividends(xTickerChoice)  # GET DIV PAY DATE, ETC
                                                        xDivExDate, xDivPayDate, xDivFreq, xDivAmount, xDivYield = xDivList
                                                        xDividend = xDivAmount
                                                else:
                                                    xDividend = '-'
                                            else:
                                                price = ticker.info['regularMarketPrice']
                                                xDividend = str(ticker.info['yield'] * 100) + '%'

                                            process_transaction(xAction, xAccountChoice, xTickerChoice, xTransDate, xTransPrice, xShares, '', '', '', '', xDivExDate, xDivPayDate, xDivFreq, xDivAmount)

                with col3:
                    if xAction == 'Sell' or xAction == 'Buy':
                        if xAccountChoice != '':
                            if xTickerChoice != '':
                                if xTransPrice > 0:
                                    if xShares > 0:
                                        st.markdown (
                                            f"""
                                            {xAction} {xTickerChoice} {xShares} Shares @ ${xTransPrice} 
                                            """
                                        )


            #-------------------------  HELD STOCKS  --------------------------
            elif xOption == 'Held Stocks':
                xStopList = getData_stockinvest()
                df = pd.DataFrame(xStopList)
                df.columns =['Ticker', 'Score', 'Rating', 'LastAction', 'Today', 'CurrentStop', 'StopLoss', 'Volatility', 'Risk']
                df = df.reindex(['Ticker','Today','CurrentStop','StopLoss','Score','Rating','LastAction','Volatility','Risk'], axis=1)

                style_negative = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('-')) {return {'color': 'red'}} 
                        else {return {'color': 'green'}}
                    };
                    """
                )
                style_currentstop = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('*')) {return {'backgroundColor': 'lavender'}} 
                    };
                    """
                )
                style_rating = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('Sell')) {return {'color': 'red'}} 
                        else if (params.value.includes('Buy')) {return {'color': 'green'}} 
                    };
                    """
                )
                style_lastaction = JsCode(
                    """
                    function(params) {
                        if (params.value.includes('Downgraded')) {return {'color': 'red'}} 
                        else if (params.value.includes('Upgraded')) {return {'color': 'green'}} 
                    };
                    """
                )
                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_default_column(groupable=True, 
                                                value=True, 
                                                enableRowGroup=True, 
                                                editable=True,
                                                enableRangeSelection=True,
                                            )
                gb.configure_column("Today", cellStyle=style_negative)
                gb.configure_column("Score", cellStyle=style_negative)
                gb.configure_column("CurrentStop", cellStyle=style_currentstop)
                gb.configure_column("Rating", cellStyle=style_rating)
                gb.configure_column("LastAction", cellStyle=style_lastaction)
                gridOptions = gb.build()
                data = AgGrid(
                    df,
                    gridOptions=gridOptions,
                    height=1000,
                    width='100%',
                    enable_enterprise_modules=True,
                    allow_unsafe_jscode=True
                )






    def display_portfolio_totals(xCntr, xAccount, xTotalValue, xTotalTodayPerc, xTotalToday, xTotalGainLoss, xTotalGainLossPerc):

        col0, buf, col1, col2, col3, col4, col5 = st.columns([0.7,0.1,1,1,1,1,1])
        #---------------  Account Name  -------------------
        with col0:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Account</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'blue'
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{xAccount}</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        #---------------  Total Value  -------------------
        with col1:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Total Value</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            xVal = str("{:,.2f}".format(xTotalValue))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>${xVal}</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        #---------------  Todays Change $  -------------------
        with col2:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Today ($)</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            if xTotalToday < 0:
                xColor = 'red'
            else:
                xColor = 'green'
            xTotalToday = str("{:,.2f}".format(xTotalToday))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>${xTotalToday}</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        #---------------  Todays Change %  -------------------
        with col3:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Today (%)</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            if xTotalTodayPerc < 0:
                xColor = 'red'
            else:
                xColor = 'green'
            x1 = str("{:,.2f}".format(xTotalTodayPerc))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{x1}%</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        with col4:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Gain/Loss ($)</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            if xTotalGainLoss < 0:
                xColor = 'red'
            else:
                xColor = 'green'
            x1 = str("{:,.2f}".format(xTotalGainLoss))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>${x1}</b></p>'
            st.markdown(row, unsafe_allow_html=True)

        with col5:
            if xCntr < 2:
                row = '<p style="font-family:sans-serif; color:RoyalBlue; margin-top: 0; margin-bottom: 5; line-height: 10px; font-size: 14px;"><b>Gain/Loss (%)</b></p>'
                st.markdown(row, unsafe_allow_html=True)
            xColor = 'black'
            if xTotalGainLossPerc < 0:
                xColor = 'red'
            else:
                xColor = 'green'
            x1 = str("{:,.2f}".format(xTotalGainLossPerc))
            row = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:{xColor}; font-size: 16px;"><b>{x1}%</b></p>'
            st.markdown(row, unsafe_allow_html=True)



    #------------------------ SAVE TRANSACTION TO GOOGLE SHEETS -----------------------#
    # def process_transaction(xAction, xAccountChoice, xTickerChoice, xTransDate, xTransPrice, xShares, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost, xDivExDate, xDivPayDate, xDivFreq, xDivAmount):

    #     with st.spinner('Loading Data...Please Wait...'):

    #         if is_prod:
    #             gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env variable
    #         else:    
    #             gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials

    #         sheet = gc.open('Research')

    #         if xAction == 'Sell':
    #             #------- Add Sale Transaction to Transactions Sheet ----------
    #             wks = sheet.worksheet_by_title('Transactions')
    #             values = [[xAccountChoice, str(xTransDate), xAction, xTickerChoice, None, xShares, xTransPrice, None, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost]]
    #             wks.append_table(values, start='A2', end=None, dimension='ROWS', overwrite=True)  # Added
    #             #------- Update Portfolio CASH Balance ----------
    #             wks = sheet.worksheet_by_title('Portfolio')
    #             for idx, row in enumerate(wks):
    #                 if (wks[idx+1][0]) == xAccountChoice:
    #                     xAmt = float(xTransPrice) * float(xShares)
    #                     if (wks[idx+1][1]) == xTickerChoice:
    #                         wks.delete_rows(idx+1, number=1)
    #                     elif (wks[idx+1][1]) == 'CASH':
    #                         xTot = wks[idx+1][10]
    #                         xTot = xTot.replace('$','')
    #                         xTot = float(xTot.replace(',',''))
    #                         wks.cell('K'+str(idx+1)).value = str(xTot + xAmt)

    #         if xAction == 'Buy':
    #             #------- Add Sale Record to Transactions Sheet ----------
    #             wks = sheet.worksheet_by_title('Transactions')
    #             values = [[xAccountChoice, str(xTransDate), xAction, xTickerChoice, None, xShares, xTransPrice, None, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost]]
    #             wks.append_table(values, start='A2', end=None, dimension='ROWS', overwrite=True)  # Added
    #             #------- Add Buy Record to Portfolio Sheet ----------
    #             wks = sheet.worksheet_by_title('Portfolio')
    #             values = [[xAccountChoice, xTickerChoice, None, str(xTransDate), xShares, xTransPrice, None, None, None, None, None, None, None, None, xDivAmount, None, None, None, xDivExDate, xDivPayDate, xDivFreq]]
    #             wks.append_table(values, start='A2', end=None, dimension='ROWS', overwrite=True)  # Added
    #             #------- Update Portfolio CASH Balance ----------
    #             for idx, row in enumerate(wks):
    #                 if (wks[idx+1][0]) == xAccountChoice:
    #                     xAmt = float(xTransPrice) * float(xShares)
    #                     if (wks[idx+1][1]) == 'CASH':
    #                         xTot = wks[idx+1][10]
    #                         xTot = xTot.replace('$','')
    #                         xTot = float(xTot.replace(',',''))
    #                         wks.cell('K'+str(idx+1)).value = str(xTot - xAmt)

    #         st.write('Transaction Processed!')

                
    def process_transaction(xAction, xAccountChoice, xTickerChoice, xTransDate, xTransPrice, xShares, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost, xDivExDate, xDivPayDate, xDivFreq, xDivAmount):

        with st.spinner('Loading Data...Please Wait...'):

            if is_prod:
                # gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') # use Heroku env variable
                var = os.getenv('GDRIVE_API_CREDENTIALS')
                st.write (var)
                st.write (eval(var))
                gc = gspread.service_account_from_dict(eval(var))
            else:    
                gc = gspread.service_account(filename='client_secret.json')

            gsheet = gc.open('Research')

            if xAction == 'Sell':
                #------- Add Sale Transaction to Transactions Sheet ----------
                values = [[xAccountChoice, str(xTransDate), xAction, xTickerChoice, None, xShares, xTransPrice, None, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost]]
                gsheet.values_append('Transactions', {'valueInputOption': 'USER_ENTERED'}, {'values': values})
                #------- Update Portfolio CASH Balance ----------
                wks = gsheet.worksheet('Portfolio')
                wksList = wks.get_all_values()
                for idx, row in enumerate(wksList):
                    if (wksList[idx][0]) == xAccountChoice:
                        xAmt = float(xTransPrice) * float(xShares)
                        if (wksList[idx][1]) == xTickerChoice:
                            wks.delete_row(idx+1)
                        elif (wksList[idx][1]) == 'CASH':
                            xTot = wksList[idx][10]
                            xTot = xTot.replace('$','')
                            xTot = float(xTot.replace(',',''))
                            wks.update_cell(idx+1, 11, str(xTot + xAmt))


            if xAction == 'Buy':
                #------- Add Sale Record to Transactions Sheet ----------
                values = [[xAccountChoice, str(xTransDate), xAction, xTickerChoice, None, xShares, xTransPrice, None, xPrevDate, xPrevShares, xPrevShareCost, xPrevTotalCost]]
                gsheet.values_append('Transactions', {'valueInputOption': 'USER_ENTERED'}, {'values': values})
                #------- Add Buy Record to Portfolio Sheet ----------
                values = [[xAccountChoice, xTickerChoice, None, str(xTransDate), xShares, xTransPrice, None, None, None, None, None, None, None, None, xDivAmount, None, None, None, xDivExDate, xDivPayDate, xDivFreq]]
                gsheet.values_append('Portfolio', {'valueInputOption': 'USER_ENTERED'}, {'values': values})
                #------- Update Portfolio CASH Balance ----------
                wks = gsheet.worksheet('Portfolio')
                wksList = wks.get_all_values()
                for idx, row in enumerate(wksList):
                    if (wksList[idx][0]) == xAccountChoice:
                        xAmt = float(xTransPrice) * float(xShares)
                        if (wksList[idx][1]) == 'CASH':
                            xTot = wksList[idx][10]
                            xTot = xTot.replace('$','')
                            xTot = float(xTot.replace(',',''))
                            wks.update_cell(idx+1, 11, str(xTot - xAmt))

            st.write('Transaction Processed!')
                




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
        pwd = st.sidebar.empty()
        t = pwd.text_input("Enter Password", type="password")
        if t != "":
            if t == 'nella1':
                pwd.empty()
                display_portfolio (xSelection)










    # # This is how you can get a Google Drive csv/excel share link to a Pandas DataFrame:
    # url = 'https://drive.google.com/file/d/1iHZZ7-8ht9Arwt2fFEdCNGGrcoq0CJ81/view?usp=sharing'
    # path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    # outlet_df = pd.read_csv(path)
    # st.write(outlet_df)


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




    # news1, news2 = st.columns([1,5])

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




            #     new_style=(df.style
            #                 .applymap(currentstop_color, subset=['CurrentStop'])
            #                 .applymap(rating_color, subset=['Rating'])
            #                 .applymap(lastaction_color, subset=['LastAction'])
            #                 .applymap(negative_red, subset=['Today', 'Score'])
            #             )
            #     st.dataframe(new_style, height=1400, width=1100)
    # def currentstop_color(x):
    #     if '*' in x:
    #         y= 'background-color: lavender'
    #     else:
    #         y= 'color: black'
    #     return y

    # def rating_color(x):
    #     if x == 'Sell Candidate':
    #         y= 'color: red'
    #     elif x == 'Strong Sell Candidate':
    #         y= 'color: red'
    #     elif x == 'Buy Candidate':
    #         y= 'color: green'
    #     elif x == 'Strong Buy Candidate':
    #         y= 'color: darkgreen'
    #     elif x == 'Hold/Accumulate':
    #         y= 'color: orange'
    #     else:
    #         y= 'color: black'
    #     return y

    # def lastaction_color(x):
    #     if x == 'Downgraded':
    #         y= 'color: red'
    #     elif x == 'Upgraded':
    #         y= 'color: green'
    #     else:
    #         y= 'color: black'
    #     return y

    # def negative_red(x):
    #     if '-' in x:
    #         y= 'color: red'
    #     else:
    #         y= 'color: green'
    #     return y