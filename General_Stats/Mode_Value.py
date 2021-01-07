import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr


#Script Overview :

#1. Make a Dataframe of Currency Pair
#2. Find the Historical Highest & Lowest Prices
#3. Finding the Mode Value


#1. Defining the Parameters (Stock / Start date / End date) and creating a Dataframe
def mode_value(stocks, endyear, endmonth, endday): 

    for stock in stocks:

        # start_date = dt.datetime(startyear, startmonth, startday)
        end_date = dt.datetime(endyear, endmonth, endday)
        
        one_year_ago = end_date - dt.timedelta(days=365)

        df = pdr.get_data_yahoo(stock, one_year_ago, end_date)


        #2. Finding the Historical Highest and Lowest values and their Midrange

        list_of_highs = df["High"].values.tolist()
        max_value = round(max(list_of_highs), 5)

        list_of_lows = df["Low"].values.tolist()
        min_value = round(min(list_of_lows), 5)

        # print(f'{stock} Highest Value:', max_value)
        # print(f'{stock} Lowest Value:', min_value)


        #3. Finding the Mode Value over a set period of time
        values = set()

        for i in list_of_highs:
            values.add(i)
        for i in list_of_lows:
            values.add(i)

        values = list(values)
        values = sorted(values)

        ans = 0
        ranges = []

        for i in range(len(values)):
            for j in range(i, (len(values))):
                curr = 0
                for k in range(len(list_of_highs)):
                    if list_of_highs[k] >= values[j] and values[i] >= list_of_lows[k]:
                        curr += 1
                    if curr > ans:
                        ans = curr
                        ranges.clear()
                        ranges.append([values[i], values[j]])
                    elif curr == ans:
                        ranges.append([values[i], values[j]])

        store = []

        for i in ranges:
            length = len(i)
            if length == 1:
                if i[length-1] not in store:
                    store.append(i[length-1])
            elif length == 2:
                if i[0] == i[1]:
                    continue
                if i not in store:
                    store.append(i)

        

        print(f'Mode of {stock} - Count : {ans} --', store)