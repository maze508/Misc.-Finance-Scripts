import datetime as dt
import pandas_datareader as pdr
from datetime import datetime
import plotly.graph_objects as go


#####################################
'''API and Setting of Parameters'''
#####################################

# Date Settings
now = datetime.now()
end_date = dt.datetime.now()
pair = 'EURUSD=X'
start_date = end_date - dt.timedelta(days=10 * 365)

# Threshold Settings
Threshold = 0.02


#################
'''DCC Process'''
#################


#Should be in main Script
def raw_data_lists(pair, start_date, end_date):
    """
    APIs from Yahoo Finance and returns arrays of useful information and details

    :param pair: Chosen Pair
    :param start_date: Start Date
    :param end_date: End Date
    :return: Arrays of Dates, Close, High, Low, Index and Dataframe
    """

    # Modifying DF Columns for Dates
    df = pdr.get_data_yahoo(pair, start_date, end_date)
    df.insert(1, "Dates", df.index, True)
    df["Modified Dates"] = df['Dates'].astype(str).str[:10]

    # Extracting DF values into a list
    list_of_close = df["Close"].values.tolist()
    list_of_highs = df["High"].values.tolist()
    list_of_lows = df["Low"].values.tolist()
    list_of_dates = df["Modified Dates"].values.tolist()
    index_list = [i for i in range(len(list_of_close))]

    return list_of_dates, list_of_close, list_of_highs, list_of_lows, index_list, df


# Should be in Main Script
def DCC_Process(list_of_dates, list_of_close, list_of_highs, list_of_lows, index_list, Threshold):
    """
    Obtains arrays of points for DC and OS Events in DCC

    :param list_of_dates: Array of dates
    :param list_of_close: Array of close prices
    :param list_of_highs: Array of high prices
    :param list_of_lows: Array of low prices
    :param index_list: Array of index values
    :param Threshold: Hyperparameter (Change in Global)
    :return: Arrays of OS and DC Points with its corresponding Dates
    """

    upturn_event = True
    # Defining initial price as highest and lowest
    highest_price = lowest_price = list_of_close[0]
    dc_points_index = []
    os_points_index = []
    os_points_list = []
    dc_points_list = []
    dc_date_list = []
    os_date_list = []
    os_up = 0
    os_down = 0

    for i in range(len(list_of_close)):
        # Defines Current Price
        current_price = list_of_close[i]

        if upturn_event:
            # If upturn event and price has reversed to a set threshold below the max price --> downturn event
            if current_price <= highest_price * (1 - Threshold):
                upturn_event = False
                # Tracks Lowest Price from now on since we are on a downturn event
                lowest_price = current_price

                # Append Current Index as DC Point Index
                dc_points_index.append(index_list[i])
                # Considering the Case if 2 DCC events occur immediately after each other
                if index_list[os_up] in os_points_index:
                    os_points_index.append(dc_points_index[-2])
                    os_up = dc_points_index[-2]
                # Normal Case where the 2 DCC events occur > 1 period apart
                else:
                    os_points_index.append(index_list[os_up])
            else:
                # During Upturn event, if current price is greater than the highest price, record it as the highest price
                if highest_price < current_price:
                    highest_price = current_price
                    os_up = i

        else:
            # if downturn event and price has reversed to a set threshold above the max price --> upturn event
            if current_price >= lowest_price * (1 + Threshold):
                upturn_event = True
                # Tracks Highest Price from now on since we are on an upturn event
                highest_price = current_price

                # Append Current Index as DC Point Index
                dc_points_index.append(index_list[i])
                # Considering the Case if 2 DCC events occur immediately after each other
                if index_list[os_down] in os_points_index:
                    os_points_index.append(dc_points_index[-2])
                    os_down = dc_points_index[-2]
                    # print('Quick Downturn Detected at Index ({}), DCC Index Value calibrated to Index ({})'
                    #       .format(i, dc_points_index[-2]))
                # Normal Case where the 2 DCC events occur > 1 period apart
                else:
                    os_points_index.append(index_list[os_down])

            else:
                # During Downturn event, if current price is lower than the lowest price, record it as the lowest price
                if lowest_price > current_price:
                    lowest_price = current_price
                    os_down = i

    # Access Indexes for List of Close and Dates for both DC and OS points
    for i in os_points_index:
        os_points_list.append(list_of_close[i])
        os_date_list.append(list_of_dates[i])
    for x in dc_points_index:
        dc_points_list.append(list_of_close[x])
        dc_date_list.append(list_of_dates[x])

    print()
    print('Number of DC and OS Points : ', len(os_points_list))
    print()

    return os_points_list, os_date_list, dc_points_list, dc_date_list


def vertical_distance(os_points_list, os_date_list, dc_points_list, dc_date_list):
    # Consider Separating it into Positive and Negative values --> Keeping track of Up/Down Trends
    """
    Checking the Price value differences between OS and DC Points for back testing Purposes

    :param os_points_list: Array of OS Points
    :param os_date_list: Array of Corresponding OS Point Dates
    :param dc_points_list: Array of DC Points
    :param dc_date_list: Array of Corresponding DC Point Dates
    :return no_of_zeroes: Number of occurrences where the difference between the current OS and current DC is 0
    :return one_count: Number of occurrences where the size of OS is at least the size of DC
    :return count: Number of occurrences where the size of the OS is at least the value of the Average Ratio of OS : DC
    """

    dc_dist_list = []
    os_dist_list = []
    percent_vertical_dist = []
    counter = 1

    # Iterating through all the DC and OS points and finding the differences between each point
    while counter < len(os_points_list):

        # Appending the DC Lengths
        dcc = abs(os_points_list[counter-1] - dc_points_list[counter-1])
        dc_dist_list.append(dcc)

        # Appending the OS Lengths
        oss = abs(os_points_list[counter] - dc_points_list[counter-1])
        os_dist_list.append(oss)

        counter += 1

    # Changing the Value to be in terms of PIPS
    if 'JPY' in pair:
        dc_dist_list = [round(i*100, 1) for i in dc_dist_list]
        os_dist_list = [round(i*100, 1) for i in os_dist_list]
    else:
        dc_dist_list = [round(i*10000, 1) for i in dc_dist_list]
        os_dist_list = [round(i*10000, 1) for i in os_dist_list]

    # Changing the OS pip distance to be of a percentage WRT the corresponding DC move
    for i in range(len(dc_dist_list)):
        percent_vertical_dist.append((round(os_dist_list[i]/dc_dist_list[i], 1)))

    # Calculating the Average Distance %
    avg_percent_vert_dist = sum(percent_vertical_dist)/len(percent_vertical_dist)

    one_count = 0
    avg_count = 0
    point_eight_count = 0
    one_point_five_count = 0 
    two_count = 0

    # Tracking the counters for various test parameters
    for i in range(len(percent_vertical_dist)):

        # Tracking if value is greater than the average % distance moved by the OS event WRT the DC event
        if percent_vertical_dist[i] >= avg_percent_vert_dist:
            avg_count += 1

        # Tracking if OS price movement is greater than the DC price movement
        if percent_vertical_dist[i] >= 1:
            one_count += 1

        # Tracking if OS price movement is greater than 80% of the DC price movement
        if percent_vertical_dist[i] >= 0.8:
            point_eight_count += 1

        if percent_vertical_dist[i] >= 1.5:
            one_point_five_count += 1
        
        if percent_vertical_dist[i] >= 2:
            two_count += 1

    # Tracking the number of occurrences where the DC Points == OS Point
    no_of_zeroes = 0
    for i in percent_vertical_dist:
        if i == 0:
            no_of_zeroes += 1

    # Prints Useful Set of Information
    # print('% Vertical Distance :', percent_vertical_dist)
    print('Average Value of OS/DC Distance :', avg_percent_vert_dist)
    print('Number of DC and OS Events :', len(percent_vertical_dist))
    print('No. of OS events where OS == 0 :', no_of_zeroes)
    print('No. of times where OS > DC by the Average Value :', avg_count)
    print('No. of times where OS > DC :', one_count)
    print('No. of times where OS is 80% of DC :', point_eight_count)
    print('No. of times where OS is 150% of DC :', one_point_five_count)
    print('No. of times where OS is 200% of DC :', two_count)

    return no_of_zeroes, one_count, avg_count








