import datetime as dt
import pandas as pd
import os
from dcc_main import DCC_Process
import yfinance as yf
import datetime as dt
import pandas_datareader as pdr
from datetime import datetime
import plotly.graph_objects as go
from dcc_main import *

''' TODO List '''

###################
'''Plotly Graphs'''
###################


# Should move this into the Graph Script
fig = go.Figure()

# Graph of OS events
fig.add_trace(go.Scatter(x=os_date_list, y=os_points_list,
                         mode='lines+markers',
                         name='OS Events'))

# Graph of DC events
fig.add_trace(go.Scatter(x=dc_date_list, y=dc_points_list,
                         mode='lines+markers',
                         name='DC Events'))

# Original Chart
fig.add_trace(go.Scatter(x=list_of_dates, y=list_of_close,
                         mode='lines+markers',
                         name='Original Chart'))

# Updating Figure Layout
fig.update_layout(
    title={
        'text': "{} (DCC = {}%)".format(pair[:-2], Threshold * 10),
        'y': 0.975,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Dates",
    yaxis_title="Price",
    font=dict(
        family='Courier New',
        color='RebeccaPurple')
)

fig.show()


