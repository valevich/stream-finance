#!/usr/bin/env python3
from bs4 import BeautifulSoup
import time
from lxml import html
import requests
import pandas as pd
from tabulate import tabulate
from urllib.request import urlopen, Request
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import yahoo_fin.stock_info as ya
from apps.stock_scrape1 import getData_Reddit
import matplotlib.pyplot as plt
from alpha_vantage.sectorperformance import SectorPerformances
from apps.stock_scrape1 import getData_MarketWatch


def app():

    st.sidebar.markdown('---')

    with st.spinner('Loading Data...Please Wait...'):

        #---------------  Header Market Data  -------------------
        symbol = 'AAPL'
        df_mw1, df_mw2, df_mw3, df_mw4 = getData_MarketWatch(symbol)
        if len(df_mw1.index) > 0:
            # new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 20px;">MarketWatch.com Markets</p>'
            # st.markdown(new_title, unsafe_allow_html=True)
            # st.table(df_mw1.assign(hack='').set_index('hack'))

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

        # Main Page Header 
        # st.markdown("""<div style='text-align: center;'><h3><b>THE STOCK ANALYSIS</b></h1></div>""", unsafe_allow_html=True)
        st.markdown("---")
        # st.markdown("")



    #---------------  Performance by Sector  -------------------
    sp = SectorPerformances(key='0E66O7ZP6W7A1LC9', output_format='pandas')
    plt.figure(figsize=(8,8))
    data, meta_data = sp.get_sector()
    # print(meta_data)
    data['Rank D: Month Performance'].plot(kind='bar')
    plt.title('30 Days Stock Market Performance (%) per Sector')
    plt.tight_layout()
    plt.grid()
    st.pyplot(plt)





    # ----------------------------------------------
    #           Market Movers Stocks   
    # ----------------------------------------------
    if st.sidebar.checkbox("Market Movers"):
        with st.spinner('Loading Data...Please Wait...'):

            # ------------- Most Active Stocks ----------------------
            st.title('Most Active Stocks')
            df1 = ya.get_day_most_active()
            df1.columns = ['Symbol', 'Name', 'Price', 'Change', 'Change_Perc', 'Volume', 'Avg_Vol_3M', 'Market_Cap', 'PE_Ratio']
            df1.fillna("",inplace=True)                                 # remove Null values from column
            df1['Change_Perc'] = df1['Change_Perc'].astype(str) + '%'   # add % to column value

            for i in df1.index:                                     
                num = human_format(df1.at[i, "Volume"])             # Reformat 'Value' Column
                df1['Volume'] = df1['Volume'].astype(str)           # Convert 'Value' Column to String
                df1.at[i, "Volume"] = num

                num = human_format(df1.at[i, "Avg_Vol_3M"])         # Reformat 'Avg Vol' Column
                df1['Avg_Vol_3M'] = df1['Avg_Vol_3M'].astype(str)   # Convert 'Avg Vol' Column to String
                df1.at[i, "Avg_Vol_3M"] = num

                if type(df1.at[i, "Market_Cap"]) != str:
                    num = human_format(df1.at[i, "Market_Cap"])     # Reformat 'Market Cap' Column
                    df1.at[i, "Market_Cap"] = num

            fig =  ff.create_table(df1)
        
            # color_schema = ['black', 'black', 'black', 'green', 'red', 'grey', 'blue']
            font_color=['black']*3 + \
                [['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['black']]
            fig = go.Figure(data=go.Table(
                columnwidth=[0.8,3,1,1,1,1.3,1.3,1.3,1],
                header=dict(values=list(['Symbol', 'Name', 'Price', 'Change', 'Change %', 'Volume', 'Avg Vol (3M)', 'Market Cap', 'PE Ratio']),
                    fill_color='#FD8E72',
                    align='center'), 
                cells=dict(values=[df1.Symbol,df1.Name,df1.Price,df1.Change,df1.Change_Perc,df1.Volume,df1.Avg_Vol_3M,df1.Market_Cap,df1.PE_Ratio],
                    fill_color='#E5ECF6',
                    # font=dict(color=color_schema),
                    font_color=font_color,
                    height=28,
                    align = ['left', 'left', 'center', 'center', 'center', 'right', 'right', 'right', 'center'])))
            fig.update_layout(margin=dict(l=25,r=5,b=0,t=10), width=900,height=600)

            st.write(fig)

    
            # ------------- Day's Gainers ----------------------
            st.title('Day\'s Gainers')
            df1 = ya.get_day_gainers()
            df1.columns = ['Symbol', 'Name', 'Price', 'Change', 'Change_Perc', 'Volume', 'Avg_Vol_3M', 'Market_Cap', 'PE_Ratio']
            df1.fillna("",inplace=True)                                 # remove Null values from column
            df1['Change_Perc'] = df1['Change_Perc'].astype(str) + '%'   # add % to column value


            for i in df1.index:                                     
                num = human_format(df1.at[i, "Volume"])             # Reformat 'Value' Column
                df1['Volume'] = df1['Volume'].astype(str)           # Convert 'Value' Column to String
                df1.at[i, "Volume"] = num

                num = human_format(df1.at[i, "Avg_Vol_3M"])         # Reformat 'Avg Vol' Column
                df1['Avg_Vol_3M'] = df1['Avg_Vol_3M'].astype(str)   # Convert 'Avg Vol' Column to String
                df1.at[i, "Avg_Vol_3M"] = num

                if type(df1.at[i, "Market_Cap"]) != str:
                    num = human_format(df1.at[i, "Market_Cap"])     # Reformat 'Market Cap' Column
                    df1['Market_Cap'] = df1['Market_Cap'].astype(str)   # Convert 'Market_Cap' Column to String
                    df1.at[i, "Market_Cap"] = num


            fig =  ff.create_table(df1)
        
            # color_schema = ['black', 'black', 'black', 'green', 'red', 'grey', 'blue']
            font_color=['black']*3 + \
                [['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['black']]
            fig = go.Figure(data=go.Table(
                columnwidth=[0.8,3,1,1,1,1.3,1.3,1.3,1],
                header=dict(values=list(['Symbol', 'Name', 'Price', 'Change', 'Change %', 'Volume', 'Avg Vol (3M)', 'Market Cap', 'PE Ratio']),
                    fill_color='#FD8E72',
                    align='center'), 
                cells=dict(values=[df1.Symbol,df1.Name,df1.Price,df1.Change,df1.Change_Perc,df1.Volume,df1.Avg_Vol_3M,df1.Market_Cap,df1.PE_Ratio],
                    fill_color='#E5ECF6',
                    # font=dict(color=color_schema),
                    font_color=font_color,
                    height=28,
                    align = ['left', 'left', 'center', 'center', 'center', 'right', 'right', 'right', 'center'])))
            fig.update_layout(margin=dict(l=25,r=5,b=10,t=10), width=900,height=800)

            st.write(fig)


            # ------------- Day's Losers ----------------------
            st.title('Day\'s Losers')
            df1 = ya.get_day_losers()
            df1.columns = ['Symbol', 'Name', 'Price', 'Change', 'Change_Perc', 'Volume', 'Avg_Vol_3M', 'Market_Cap', 'PE_Ratio']
            df1.fillna("",inplace=True)                                 # remove Null values from column
            df1['Change_Perc'] = df1['Change_Perc'].astype(str) + '%'   # add % to column value

            for i in df1.index:                                     
                num = human_format(df1.at[i, "Volume"])             # Reformat 'Value' Column
                df1['Volume'] = df1['Volume'].astype(str)           # Convert 'Value' Column to String
                df1.at[i, "Volume"] = num

                num = human_format(df1.at[i, "Avg_Vol_3M"])         # Reformat 'Avg Vol' Column
                df1['Avg_Vol_3M'] = df1['Avg_Vol_3M'].astype(str)   # Convert 'Avg Vol' Column to String
                df1.at[i, "Avg_Vol_3M"] = num

                if type(df1.at[i, "Market_Cap"]) != str:
                    num = human_format(df1.at[i, "Market_Cap"])     # Reformat 'Market Cap' Column
                    df1['Market_Cap'] = df1['Market_Cap'].astype(str)   # Convert 'Avg Vol' Column to String
                    df1.at[i, "Market_Cap"] = num
                # num = human_format(df1.at[i, "Market_Cap"])         # Reformat 'Avg Vol' Column
                # df1['Market_Cap'] = df1['Market_Cap'].astype(str)   # Convert 'Avg Vol' Column to String
                # df1.at[i, "Market_Cap"] = num
 
 
            fig =  ff.create_table(df1)
        
            # color_schema = ['black', 'black', 'black', 'green', 'red', 'grey', 'blue']
            font_color=['black']*3 + \
                [['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['black']]
            fig = go.Figure(data=go.Table(
                columnwidth=[0.8,3,1,1,1,1.3,1.3,1.3,1],
                header=dict(values=list(['Symbol', 'Name', 'Price', 'Change', 'Change %', 'Volume', 'Avg Vol (3M)', 'Market Cap', 'PE Ratio']),
                    fill_color='#FD8E72',
                    align='center'), 
                cells=dict(values=[df1.Symbol,df1.Name,df1.Price,df1.Change,df1.Change_Perc,df1.Volume,df1.Avg_Vol_3M,df1.Market_Cap,df1.PE_Ratio],
                    fill_color='#E5ECF6',
                    # font=dict(color=color_schema),
                    font_color=font_color,
                    height=28,
                    align = ['left', 'left', 'center', 'center', 'center', 'right', 'right', 'right', 'center'])))
            fig.update_layout(margin=dict(l=25,r=5,b=10,t=10), width=900,height=800)

            st.write(fig)


    # ------------------------------------------------------------
    #           Reddit Wall Street Bets Trending Stocks   
    # ------------------------------------------------------------
    if st.sidebar.checkbox("Wall Street Bets"):
        with st.spinner('Loading Data...Please Wait...'):

            st.title('Reddit Wall Street Bets')
            xtitle = '<p style="font-family:sans-serif; font-size: 16px;">Trending NYSE and NASDAQ listed companies for the past 5 hours on WSB.</p>'
            st.markdown(xtitle, unsafe_allow_html=True)
            # st.sidebar.markdown("""<div style='text-align: center;'>Wall Street Bets</div>""", unsafe_allow_html=True)
            # st.sidebar.markdown('---')

            df5, asOfTime = getData_Reddit()

            xTimeLine = f'<p style="font-family:sans-serif; margin-top: 0; margin-bottom: 10;line-height: 2px; font-size: 14px;">Last updated: {asOfTime}</p>'
            st.markdown(xTimeLine, unsafe_allow_html=True)
            st.write ('\n\n')

            fig =  ff.create_table(df5)
        
            color_schema = ['black', 'black', 'black', 'green', 'red', 'grey', 'blue']
            fig = go.Figure(data=go.Table(
                columnwidth=[1,6,3,1,1,1,1],
                header=dict(values=list(df5[['Ticker','Company','Industry','Buy','Sell','Hold','Total']].columns),
                    fill_color='#FD8E72',
                    align='center'), 
                cells=dict(values=[df5.Ticker,df5.Company,df5.Industry,df5.Buy,df5.Sell,df5.Hold,df5.Total],
                    fill_color='#E5ECF6',
                    font=dict(color=color_schema),
                    height=28,
                    align = ['left', 'left', 'center'])))

            # fig.update_layout(margin=dict(l=25,r=5,b=10,t=10), width=900,height=600)
            fig.update_layout(margin=dict(l=25,r=5,b=0,t=10), width=900,height=600)
            st.write(fig)



    # ------------------------------------------------------------
    #           Twitter Sentiment   
    # ------------------------------------------------------------
    if st.sidebar.checkbox("Twitter Sentiment"):
        with st.spinner('Loading Data...Please Wait...'):

            st.title('Twitter Sentiment')
            xtitle = '<p style="font-family:sans-serif; font-size: 16px;">Most Active Market Gainers with Twitter Feedback</p>'
            st.markdown(xtitle, unsafe_allow_html=True)


            #-----------------------------------------------------------------------------------------------
            # Get the 100 most traded stocks for the trading day
            movers = ya.get_day_most_active()

            #-----------------------------------------------------------------------------------------------
            #   The yahoo_fin package is able to provide the top 100 stocks with the largest trading volume. 
            #   We are interested in stocks with a positive change in price so let’s filter based on that.
            movers = movers[movers['% Change'] >= 0]
            movers.head()
            # print (movers)

            #-----------------------------------------------------------------------------------------------
            #   It is often a good idea to see if those stocks are also generating attention, and what kind 
            #   of attention it is to avoid getting into false rallies. We will scrap some sentiment data 
            #   courtesy of sentdex. Sometimes sentiments may lag due to source e.g News article published 
            #   an hour after the event, so we will also utilize tradefollowers for their twitter sentiment 
            #   data. We will process both lists independently and combine them. For both the sentdex and 
            #   tradefollowers data we use a 30 day time period.
            #   NOTE: Sentdex only has stocks which belong to the S&P 500
            res = requests.get('http://www.sentdex.com/financial-analysis/?tf=30d')
            soup = BeautifulSoup(res.text, "html.parser")
            table = soup.find_all('tr')

            stock = []
            sentiment = []
            mentions = []
            sentiment_trend = []

            for ticker in table:
                ticker_info = ticker.find_all('td')
                
                try:
                    stock.append(ticker_info[0].get_text())
                except:
                    stock.append(None)
                try:
                    sentiment.append(ticker_info[3].get_text())
                except:
                    sentiment.append(None)
                try:
                    mentions.append(ticker_info[2].get_text())
                except:
                    mentions.append(None)
                try:
                    if (ticker_info[4].find('span',{"class":"glyphicon glyphicon-chevron-up"})):
                        sentiment_trend.append('up')
                    else:
                        sentiment_trend.append('down')
                except:
                    sentiment_trend.append(None)
                    
            company_info = pd.DataFrame(data={'Symbol': stock, 'Sentiment': sentiment, 'direction': sentiment_trend, 'Mentions':mentions})
            company_info


            #   We then combine these results with our previous results about the most traded stocks 
            #   with positive price changes on a given day. This done using a left join of this data 
            #   frame with the original movers data frame
            top_stocks = movers.merge(company_info, on='Symbol', how='left')
            top_stocks.drop(['Market Cap','PE Ratio (TTM)'], axis=1, inplace=True)
            top_stocks
            # print (top_stocks)


            #-----------------------------------------------------------------------------------------------
            #   A couple of stocks pop up with both very good sentiments and an upwards trend in favourability.
            #   The mentions here refer to the number of times the stock was referenced according to the 
            #   internal metrics used by sentdex. Let's attempt supplimenting this information with some data based
            #   on twitter. We get stocks that showed the strongest twitter sentiments with a time period of 1 month.
            res = requests.get("https://www.tradefollowers.com/strength/twitter_strongest.jsp?tf=1m")
            soup = BeautifulSoup(res.text, "html.parser")
            stock_twitter = soup.find_all('tr')

            twit_stock = []
            sector = []
            twit_score = []

            for stock in stock_twitter:
                try:
                    score = stock.find_all("td",{"class": "datalistcolumn"})
                    twit_stock.append(score[0].get_text().replace('$','').strip())
                    sector.append(score[2].get_text().replace('\n','').strip())
                    twit_score.append(score[4].get_text().replace('\n','').strip())
                except:
                    twit_stock.append(np.nan)
                    sector.append(np.nan)
                    twit_score.append(np.nan)
                    
            twitter_df = pd.DataFrame({'Symbol': twit_stock, 'Sector': sector, 'Twit_Bull_score': twit_score})

            # Remove NA values 
            twitter_df.dropna(inplace=True)
            twitter_df.drop_duplicates(subset ="Symbol", 
                                keep = 'first', inplace = True)
            twitter_df.reset_index(drop=True,inplace=True)
            twitter_df
            # print (twitter_df)



            #-----------------------------------------------------------------------------------------------
            #   Twit_Bull_score refers to the internally scoring used at tradefollowers to rank stocks based on 
            #   twitter sentiments, and can range from 1 to as high as 10,000 or greater. With the twitter 
            #   sentiments obtains, we combine it with our sentiment data to get an overall idea of the data.
            Final_list =  top_stocks.merge(twitter_df, on='Symbol', how='left')
            Final_list
            # print (Final_list)



            #-----------------------------------------------------------------------------------------------
            #   Finally, we include a twitter momentum score.
            res2 = requests.get("https://www.tradefollowers.com/active/twitter_active.jsp?tf=1m")
            soup2 = BeautifulSoup(res2.text, "html.parser")

            stock_twitter2 = soup2.find_all('tr')

            twit_stock2 = []
            sector2 = []
            twit_score2 = []

            for stock in stock_twitter2:
                try:
                    score2 = stock.find_all("td",{"class": "datalistcolumn"})
                    
                    
                    
                    twit_stock2.append(score2[0].get_text().replace('$','').strip())
                    sector2.append(score2[2].get_text().replace('\n','').strip())
                    twit_score2.append(score2[4].get_text().replace('\n','').strip())
                except:
                    twit_stock2.append(np.nan)
                    sector2.append(np.nan)
                    twit_score2.append(np.nan)
                    
            twitter_df2 = pd.DataFrame({'Symbol': twit_stock2, 'Sector': sector2, 'Twit_mom': twit_score2})

            # Remove NA values 
            twitter_df2.dropna(inplace=True)
            twitter_df2.drop_duplicates(subset ="Symbol", 
                                keep = 'first', inplace = True)
            twitter_df2.reset_index(drop=True,inplace=True)
            twitter_df2
            # print (twitter_df2)



            #-----------------------------------------------------------------------------------------------
            #   We again combine the dataframes to earlier concatanated dataframes. This will form our recommender list
            Recommender_list = Final_list.merge(twitter_df2, on='Symbol', how='left')
            # Recommender_list.drop(['Volume','Avg Vol (3 month)'],axis=1, inplace=True)
            Recommender_list
            # print ("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            # print ("                                                                Stock Market Screening and Analysis                                                                   ")
            # print ("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            # print (Recommender_list.to_string())
            # print ("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")


            df1 = Recommender_list
            df1.drop(['Volume','Avg Vol (3 month)','Sector_x'],axis=1, inplace=True)
            df1.columns = ['Symbol', 'Name', 'Price', 'Change', 'Change_Perc', 'Sentiment', 'Direction', 'Mentions', 'Twit_Bull_score', 'Sector', 'Twit_mom']

            df1.fillna("",inplace=True)                                 # remove Null values from column
            df1['Change_Perc'] = df1['Change_Perc'].astype(str) + '%'   # add % to column value

            fig =  ff.create_table(df1)
        
            # color_schema = ['black', 'black', 'black', 'green', 'red', 'grey', 'blue']
            font_color=['black']*3 + \
                [['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Change_Perc'].str.contains('-')],
                ['black']]
            fig = go.Figure(data=go.Table(
                columnwidth=[1,3,1,1,1,1.2,1.2,1.2,1,1,2.4],
                header=dict(values=list(['Symbol', 'Name', 'Price', 'Change', 'Change %', 'Sentiment', 'Trend', 'Mentions', 'TW Bull Score', 'TW Moment', 'Sector']),
                    fill_color='#FD8E72',
                    align='center'), 
                cells=dict(values=[df1.Symbol,df1.Name,df1.Price,df1.Change,df1.Change_Perc,df1.Sentiment,df1.Direction,df1.Mentions,df1.Twit_Bull_score,df1.Twit_mom,df1.Sector],
                    fill_color='#E5ECF6',
                    # font=dict(color=color_schema),
                    font_color=font_color,
                    height=28,
                    align = ['left', 'left', 'center'])))
            fig.update_layout(margin=dict(l=0,r=0,b=10,t=10), width=900,height=800)

            st.write(fig)


def human_format(num):
    num = float(num)
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])



