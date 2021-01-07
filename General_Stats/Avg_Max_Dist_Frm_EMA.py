import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import pandas_datareader as pdr


'''Script Overview'''

'''
1. Make a Dataframe of Currency Pair
2. Adding EMA Column (Desired Period and Number) to the DF
3. Finding the Max Points of Price from the EMA and finding the average value
'''


#0. Workaround for Obtaining data from Yahoo Finance as they changed the way they obtain data
yf.pdr_override()


#1. Defining the Parameters (Stocks / Start date / End date) and creating a Dataframe
stocks = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X', 'USDJPY=X', 'USDCHF=X', 'USDCAD=X']

for stock in stocks:
    startyear = 2015
    startmonth = 1
    startday = 1

    start_date = dt.datetime(startyear, startmonth, startday)
    end_date_now = dt.datetime.now()
    # Another Choice if don't want to measure to current time
    # end_date = dt.datetime(2020, 1, 1)

    df = pdr.get_data_yahoo(stock, start_date, end_date_now)


    #2. Adding an EMA column to the data table
    ema_list = [200]
    for ema in ema_list:
        emaString = "Ema_" + str(ema)

        df[emaString] = df.iloc[:, 5].ewm(span=ema, adjust=True).mean()
        # print(df)


        #3a. Finding the Distance where the price is above/below the EMA and appending the distance between the extreme points to a list
        list_High = []

        for i in df.index:
            # If the Candles are Below EMA, return me a list of the Pip Difference
            if (df["Low"][i] > df[emaString][i]):
                diff_higher = df["High"][i] - df[emaString][i]
                diff_higher_array = np.array(diff_higher)
                diff_higher_values = round(diff_higher_array * 10000, 2)
                list_High.append(diff_higher_values)

            # If the Candles are Above EMA, return me a list of the Pip Difference
            elif (df["High"][i] < df[emaString][i]):
                diff_lower = df["Low"][i] - df[emaString][i]
                diff_lower_array = np.array(diff_lower)
                diff_lower_values = round(diff_lower_array * 10000, 2)
                list_High.append(diff_lower_values)

            # If the Candles are Touching EMA, return me a list of 0's
            elif (df["Low"][i] <= df[emaString][i] <= df["High"][i]):
                list_High.append(0)


        #3b. Makes the list values absolute and cuts the first 'ema' number of values for accuracy
        abs_list = [abs(element) for element in list_High]


        #3c. Finding the Max Values When Price leaves EMA
        output_list = []
        values_to_append = []

        for i in abs_list:
            if i == 0:
                if values_to_append == []:
                    pass
                else:
                    output_list.append(values_to_append)
                    values_to_append = []
            else:
                values_to_append.append(i)

        maxvalue = [max(i) for i in output_list]


        #3d. If the max distance is less than 10 pips, remove the value

        moderated_max = [i for i in maxvalue]
        for i in moderated_max:
            if int(i) < 10:
                moderated_max.remove(i)
        average_moderated_maxdistance = sum(moderated_max) / len(moderated_max)







        '''ALTERNATIVE 1 '''

            #list2 = [i for i, x in enumerate(abs_list) if x == 0]
            #ans = []
            #index = 0
            #while index < len(list2) - 1:
            #    maximum = 0
            #    for i in range(list2[index], list2[index]+1):
            #        maximum = max(maximum, abs_list[i])
            #    ans.append(maximum)
            #    index += 1

        '''ALTERNATIVE 2 '''

            # ans = []
            # maximum = 0
            # for i in range(len(abs_list)):
            #     if list[i] == 0:
            #         ans.append(maximum)
            #         maximum = 0
            #         maximum = max(maximum, abs_list[i])
            #     ans.append(maximum)


        #3e. Obtaining the Average Value for the Max Distance Price moves away from the EMA
        average_maxdistance_from_ema = sum(maxvalue) / len(maxvalue)
        if 'JPY' in stock:
            average_maxdistance_from_ema_JPY = average_maxdistance_from_ema / 100
            average_moderated_maxdistance_JPY = average_moderated_maxdistance / 100
            print(f'{stock} Average Max Distance from {ema} EMA:', average_maxdistance_from_ema_JPY)
            print(f'{stock} Moderated Max Distance from {ema} EMA:', average_moderated_maxdistance_JPY)
            print('***************************************************************')
        else:
            print(f'{stock} Average Max Distance from {ema} EMA:', average_maxdistance_from_ema)
            print(f'{stock} Moderated Max Distance from {ema} EMA:', average_moderated_maxdistance)
            print('****************************************************************')