#------------------   Included code from stream18.py   ----------------------
#------------------   Included code from stream19.py (Sidebar)  ----------------------
#------------------   Included code from stream17.py (TA Chart)  ----------------------
#------------------   Included code from stream6.py (Bollinger Bands)  ----------------------
#------------------   Included code from stream10.py (Stock Price Graph)  ----------------------
import streamlit as st 
import requests
import yfinance as yf 
import plotly.graph_objects as go 
import plotly.express as px 
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import datetime
import cufflinks as cf
from datetime import date
import markdown


from apps.stock_scrape1 import getData_Zacks
from apps.stock_scrape1 import getData_Dividata
from apps.stock_scrape1 import getData_Tipranks
from apps.stock_scrape1 import getData_StockInvest
from apps.stock_scrape1 import getData_MarketWatch


def app():
    # st.title('Stock Summary')

    # st.set_page_config(layout="wide") #wide width of page 


    #################### SIDEBAR FUNCTIONS ####################

    #------ Function to SCRAPE INFO ON TICKER
    @st.cache
    def get_info(symbol):
        url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        # locations of values, all have same class
        indices = [0, 1, 5, 13, 8, 10, 11]
        try:
            info = [soup.find_all('td', {'class': "Ta(end) Fw(600) Lh(14px)"})[i].text for i in indices]
            # company = soup.find_all('h1', {'class': "D(ib) Fz(18px)"})[0].text
            # name_len = len(company) - (len(symbol) + 2) #remove ticker at end
            # info.insert(0, company[:name_len]) #add company name at front
        except:
            info = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
        return info


    #------ Function to SCRAPE CURRENT PRICE AND CHANGE
    @st.cache
    def get_price(symbol):
        url = f"https://finance.yahoo.com/quote/{symbol}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            for stock in soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'):
                currentPrice = stock.get_text()
            changePrice = soup.find('span', {'class': ['Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)',
                                                    'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)']}).text
            # print(currentPrice)
            # print(changePrice)
        except:
            currentPrice = ['N/A']
            changePrice = ['N/A']
        return currentPrice, changePrice



    #------ Function to DISPLAY TICKER VALUES
    def display_summary(symbol):
        info = get_info(symbol)
        price = get_price(symbol)

        row = \
        f"""<div> 
                <span style='float: left; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{"Today's Price: "}</b></span>
                <span style='float: right; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:18px'><b>{price[0]}</b></span>
            </div>
        """
        st.markdown(row, unsafe_allow_html=True)
        
        if price[1][0:1] == '+':
            row = \
            f"""<div> 
                    <span style='float: right; color: green; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{price[1]}</b></span>
                </div>
            """
        else:
            row = \
            f"""<div> 
                    <span style='float: right; color: red; margin-top: 0; margin-bottom: 0; line-height: 10px; font-size:14px'><b>{price[1]}</b></span>
                </div>
            """
        st.markdown(row, unsafe_allow_html=True)
        
        st.markdown('\n')

        info_names = ["Close Price: ", "Open Price: ", "52-Week Range: ", "Dividend Rate & Yield: ", \
            "Market Cap: ", "PE Ratio: ", "EPS: "]
        for name,infoValue in zip(info_names, info):
            row = \
            f"""<div> 
                    <span style='float: left;line-height: 10px; font-size:12px'><b>{name}</b></span>
                    <span style='float: right;line-height: 10px; font-size:12px'> {infoValue}</span>
                </div>
            """
            st.markdown(row, unsafe_allow_html=True)
        # st.markdown("---")



    #------------------------ SETUP SIDEBAR TICKER INPUT -----------------------#
    # symbol = st.text_input('Enter Ticker: ', value = 'AAPL')
    # ticker = yf.Ticker(symbol)

    # # Load ticker symbols
    # alltickers_df = pd.read_csv("tickers.csv")
    # tickers = list(alltickers_df['Symbol'])

    # st.sidebar.markdown("""<h2 style='text-align: center;'>SEARCH 🔎</h2>""", unsafe_allow_html=True)
    with st.spinner('Loading Data...Please Wait...'):
        symbol = st.sidebar.text_input('Stock Symbol', value = 'AAPL') #search box

        ticker = yf.Ticker(symbol)

        if not symbol.isupper():
            symbol = symbol.upper()

        # if no ticker entered
        if not symbol: 
            st.sidebar.markdown('')
            st.sidebar.markdown("""<div style='text-align: center;'>Please search a ticker to see results.</div>""", unsafe_allow_html=True)
        else: 
            # Sidebar
            st.sidebar.markdown('---')
            # display_summary(symbol)


    #---------------  TOP HEADER  -------------------

    #---------------  Header Market Data  -------------------
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
            if '-' in df_mw1.iloc[1]['Change']:
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


    #---------------  2 Header Column Section  -------------------
    if symbol: 
        hdr1,hdr2,hdr3 = st.beta_columns([1,3,2])
        with hdr1:
            if ticker.info['logo_url']:
                st.image(ticker.info['logo_url'])
        with hdr2: 
            try:
                st.subheader(ticker.info['longName'])
                xIndustry = ticker.info['sector'] + " - " + ticker.info['industry']
                row = f'<p style="font-family:sans-serif; float: left;line-height: 16px; font-size: 14px;">{xIndustry}</p>'
                st.markdown(row, unsafe_allow_html=True)
            except:
                pass
        with hdr3:
            display_summary(symbol)

        summ = ticker.info['longBusinessSummary']
        with st.beta_expander(f'Description: {summ[0:250]} ... Read more'):
            st.markdown(f'<p class="small-font"> {summ} !!</p>', unsafe_allow_html=True)

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
        if symbol: 

            #--------  Display Stock Price Graph ----------------- 
            start = "2021-01-01" # start of graphics                   #
            today = date.today()+ datetime.timedelta(days=1)
            d1 = today.strftime("%Y-%m-%d")
            current_year, current_month, current_day = today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")
            tickerData = yf.download(symbol, start=start, end="{}".format(d1))
            tickerData['Date']=tickerData.index
            df1 = tickerData

            # window choice
            xRange = st.sidebar.slider('Select Range (days)', min_value=2,max_value=126, value=30)
            # st.title('Share price of last '+str(xRange)+' days\n')
            st.subheader('Share price of last '+str(xRange)+' days\n')
        
            vert = '#599673'
            rouge = '#e95142'

            fig = make_subplots(rows=1, cols=2,
                                specs=[[{'type': 'xy'},{'type':'indicator'}] for i in range (1)],
                                column_widths=[0.85, 0.15],
                                shared_xaxes=True,
                                subplot_titles=[symbol, ''])

            def xColor(df):
                if df['Close'].iloc[-1*xRange]-df['Close'].iloc[-1] < 0 :
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

            st.plotly_chart(fig)
            st.write ('\n\n\n')


            #--------  Display Return vs SP500 ----------------- 
            st.subheader('Percent Return vs SP500')
            per_return = px.line(new_df, x='Date', y=new_df.columns)
            per_return.update_layout(autosize=True,width=1000)
            st.write(per_return)




    #---------------  Technicals Selection  -------------------
    if st.sidebar.checkbox("Technicals"):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol: 

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
                #st.table(show)
                #st.line_chart(df.Close)
                #st.write(data)


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
    if st.sidebar.checkbox("Fundamentals"):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol: 
                st.header(f'{symbol.upper()} Fundamentals')
                choice = st.sidebar.selectbox('Quarterly or Yearly Financials',['Yearly','Quarterly'])

                left, right = st.beta_columns(2)
                with left: 
                    st.write('Market Cap:   ', ticker.info['marketCap'])            
                    try: 
                        st.write('Trailing P/E: ', ticker.info['trailingPE'])
                    except KeyError as e: 
                        st.write('Trailing P/E: None ')
                    st.write('Dividend Rate:', ticker.info['dividendRate'])
                    st.write('Book Value:   ', ticker.info['bookValue'])
                with right: 
                    st.write('Price to Sales: ',ticker.info['priceToSalesTrailing12Months'])
                    st.write('Forward P/E: ',   ticker.info['forwardPE'])
                    if ticker.info['dividendYield']:
                        st.write('Dividend Yield (%): ',ticker.info['dividendYield'] * 100)
                    else:
                        st.write('Dividend Yield (%): ',ticker.info['dividendYield'])
                    st.write('Price to Book: ', ticker.info['priceToBook'])

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

        st.write ('\n\n\n')




    #---------------  Analyst Recommendations  -------------------
    if st.sidebar.checkbox("Analyst Ratings"):
        with st.spinner('Loading Data...Please Wait...'):
            if symbol: 

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
                    # st.table(df_mw3.assign(hack='').set_index('hack'))
                    # st.write(df_mw3)

                    # background_color = '#F5F5F5'
                    # st.title('A Closer look into data')
                    fig = go.Figure(data=go.Table(
                        columnwidth=[3,2,2,2],
                        header=dict(values=list(df_mw3[['Rating','Current','One_Month_Ago','Three_Month_Ago']].columns),
                            fill_color='#FD8E72',
                            align='center'), 
                        cells=dict(values=([df_mw3.Rating,df_mw3.Current,df_mw3.One_Month_Ago,df_mw3.Three_Month_Ago]),
                            fill_color='#E5ECF6',
                            align='left')))

                    # fig.update_layout(margin=dict(l=5,r=5,b=10,t=10),
                    #     paper_bgcolor = background_color)
                    fig.update_layout(margin=dict(l=60,r=1,b=1,t=10))

                    st.write(fig)


    if st.sidebar.checkbox("Add'l Sources"):
        if symbol: 

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

            st.markdown('---')





