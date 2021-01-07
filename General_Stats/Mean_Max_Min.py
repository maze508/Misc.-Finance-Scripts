import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import pandas_datareader as pdr

#Script Overview :

#1. Make a Dataframe of Currency Pair
#2. Find the Historical Highest & Lowest Prices
#3. Find the Historical Mean/Average Value of Price




#0. Workaround for Obtaining data from Yahoo Finance as they changed the way they obtain data
yf.pdr_override()


#1. Defining the Parameters (Stock / Start date / End date) and creating a Dataframe
stocks = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X', 'USDJPY=X', 'USDCHF=X', 'USDCAD=X']

for stock in stocks:
    startyear = 2018
    startmonth = 1
    startday = 1

    start_date = dt.datetime(startyear, startmonth, startday)
    end_date = dt.datetime.now()

    df = pdr.get_data_yahoo(stock, start_date, end_date)


    #2. Finding the Historical Highest and Lowest values and their Midrange
    list_of_highs = df["High"].values.tolist()
    max_value = round(max(list_of_highs), 5)

    list_of_lows = df["Low"].values.tolist()
    min_value = round(min(list_of_lows), 5)

    print(f'{stock} Highest Value:', max_value)
    print(f'{stock} Lowest Value:', min_value)


    #3. Finding the Historical Mean/Average Value by finding the mean of the average of highs and lows :
    average_of_highs = sum(list_of_highs) / len(list_of_highs)
    average_of_lows = sum(list_of_lows) / len(list_of_lows)
    mean_value = round((average_of_highs + average_of_lows) / 2, 5)

    print(f'{stock} Mean Value:', mean_value)
    print('*********************************')