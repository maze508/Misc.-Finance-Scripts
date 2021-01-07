import yfinance as yf
import datetime as dt
import pandas_datareader as pdr
from datetime import datetime
import plotly.graph_objects as go
from dcc_combined import *

list_of_dates, list_of_close, list_of_highs, list_of_lows, index_list, df = raw_data_lists(pair, start_date, now)

os_points_list, os_date_list, dc_points_list, dc_date_list = DCC_Process(list_of_dates, list_of_close, list_of_highs,
                                                                         list_of_lows, index_list, Threshold)

no_of_zeroes, one_count, avg_count = vertical_distance(os_points_list, os_date_list, dc_points_list, dc_date_list)