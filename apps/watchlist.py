import streamlit as st
import pandas as pd
import pygsheets
from pygsheets.datarange import DataRange
import plotly.graph_objects as go


def app():

    st.sidebar.markdown('---')

    # if st.sidebar.checkbox("Test"):
    #     gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials
    #     sheet = gc.open('Research')
    #     wks = sheet.worksheet_by_title('Watchlist')
    #     df1 = wks.get_as_df()
    #     st.table (df1)

        # wks.update_value('A40', "Testing")



    if st.sidebar.checkbox("My Watchlist"):

        with st.spinner('Loading Data...Please Wait...'):

            st.title('My Watchlist')

            gc = pygsheets.authorize(service_file='client_secret.json') # using service account credentials
            sheet = gc.open('Research')
            wks = sheet.worksheet_by_title('Watchlist')

            df1 = wks.get_as_df()

            df1.drop(
                columns=["7_day_Change", "30_day_Change", "90_day_Change"]
            )

            font_color = ['black'] * 6 + \
                [['red' if  boolv else 'green' for boolv in df1['Today_Perc'].str.contains('-')],
                ['red' if  boolv else 'green' for boolv in df1['Gain_Loss'].str.contains('-')],
                ['black']]

            fig = go.Figure(data=[go.Table(
                columnwidth=[1.2,5,1.7,0.7,1.3,1.3,1.3,1.3,2,1.3,1.3,1.3,1.3,1.3,1.3,1.3],
                header=dict(values=list(['Symbol', 'Name', 'Buy Date', 'Shrs', 'Cost', 
                                        'Today', 'Today %', 'Gain/Loss', 'Dividend (Yield)',
                                        '52-Week Low', '52-Week High', 'EPS', 'PE',
                                        'Mkt Cap', 'Out Shares', 'Volume']),
                            fill_color='paleturquoise',
                            align='center'),
                cells=dict(values=[df1.Ticker, df1.Company, df1.Buy_Date, df1.Shares,
                                df1.Cost, df1.Today, df1.Today_Perc, df1.Gain_Loss,
                                df1.Dividend_Yield, df1.Low_52_wk, df1.High_52_wk, df1.EPS,
                                df1.PE, df1.Mkt_Cap, df1.Out_Shares, df1.Volume, ],
                        fill_color='lavender',
                        font_color=font_color,
                        height=25,
                        align = ['left', 'left', 'center', 'center', 'right']
                    )
                )
            ])

            # fig.show()
            fig.update_layout(margin=dict(l=0,r=0,b=5,t=5), width=1300,height=800)
            st.write(fig)










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
