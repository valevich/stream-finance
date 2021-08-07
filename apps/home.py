import streamlit as st
import pandas as pd
import numpy as np
from apps.stock_scrape1 import getData_MarketWatch
import requests
from bs4 import BeautifulSoup as bs


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
        # st.markdown("""<div style='text-align: center;'><h3><b>THE STOCK ANALYSIS</b></h1></div>""", unsafe_allow_html=True)
        st.markdown("---")
        # st.markdown("")


        #---------------  Latest News  -------------------
        url = 'https://finance.yahoo.com/topic/stock-market-news'
        res = requests.get(url)
        soup = bs(res.content, 'lxml')

        xList2 = []
        for news in soup.find_all('li', class_='js-stream-content Pos(r)'):
            images = news.find_all('img')
            xNewsSource = news.find('div', class_='C(#959595) Fz(11px) D(ib) Mb(6px)')
            xHeadline = news.find('h3', class_='Mb(5px)')
            xDetails = news.find('p', class_='Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)')
            if xNewsSource:

                xList = []

                xNewsSource = xNewsSource.get_text()
                xList.append(xNewsSource)
                print("========================================")
                print("NewsSource: " + xNewsSource)

                if xHeadline:
                    xHeadline = xHeadline.get_text()
                    xList.append(xHeadline)
                    print("Headline: " + xHeadline)
                else:
                    xList.append(' ')

                if xDetails:
                    xDetails = xDetails.get_text()
                    xList.append(xDetails)
                    print("Details: " + xDetails)
                else:
                    xList.append(' ')

                for link in news.find_all('a', href=True):
                    xNewsLink = 'https://finance.yahoo.com' + link['href']
                    xList.append(xNewsLink)
                    print("NewsLink: " + xNewsLink)

                for image in images:
                    if image['src']:
                        xNewsImage = image['src']
                        xList.append(xNewsImage)
                        print ('NewsImage: ' + xNewsImage)
    
                xList2.append(xList)


        for xIdx, elem in enumerate(xList2):
            News(xIdx, xList2)

        st.write ('\n\n')



def News(xIdx, xList2):

    news1, news2 = st.beta_columns([1,5])

    with news1:
        try:
            st.image(xList2[xIdx][4])
        except:
            st.image('https://cdn.pixabay.com/photo/2016/10/10/22/38/business-1730089_1280.jpg')

    with news2: 
        source = xList2[xIdx][0]
        text = xList2[xIdx][1]
        link = xList2[xIdx][3]
        details = xList2[xIdx][2]
        st.markdown(
            f"""
                <p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:black; font-size: 12px;">{source}</p>
            """, unsafe_allow_html=True,
        )
        st.markdown(
            f"""
                <p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:black; font-size: 18px;"><a href="{link}">{text}</a></p>
            """, unsafe_allow_html=True,
        )
        st.markdown(
            f"""
                <p style="font-family:sans-serif; margin-top: 0; margin-bottom: 0; color:black; font-size: 14px;">{details}</p>
            """, unsafe_allow_html=True,
        )

        st.markdown("***")


