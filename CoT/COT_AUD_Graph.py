import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import quandl
import datetime as dt
from matplotlib import pyplot as plt
import plotly.express as px
import numpy as np

'''
Pandas Data Frame Creation
'''

auth_tok = "``` Insert Quandl Token Here  ```"
CoT_Key = ['CFTC/099741_F_L_ALL', 'CFTC/096742_F_L_ALL', 'CFTC/232741_F_L_ALL', 'CFTC/112741_F_L_ALL', 'CFTC/097741_F_L_ALL', 'CFTC/092741_F_L_ALL', 'CFTC/090741_F_L_ALL']
CoT_Key_Change = ['CFTC/099741_F_L_CHG', 'CFTC/096742_F_L_CHG', 'CFTC/232741_F_L_CHG', 'CFTC/112741_F_L_CHG', 'CFTC/097741_F_L_CHG', 'CFTC/092741_F_L_CHG', 'CFTC/090741_F_L_CHG']
CoT_Cur = ['EUR', "GBP", "AUD", "NZD", "JPY", "CHF", "CAD"]
this_friday = dt.date.today()
last_friday = this_friday - dt.timedelta(days=13)
last_fiveyears = this_friday - dt.timedelta(days=(365*5)+13)


data = quandl.get(CoT_Key[2], trim_start=last_fiveyears, trim_end=this_friday, authtoken=auth_tok)
data.insert(0, "Currency", "AUD", True)

data2 = quandl.get(CoT_Key_Change[2], trim_start=last_fiveyears, trim_end=this_friday, authtoken=auth_tok)
data2.insert(0, "Currency", "AUD", True)



data.insert(1, "Dates", data.index, True)
data["Modified Dates"] = data['Dates'].astype(str).str[:10]

cols = data.columns.tolist()
cols.insert(0, cols.pop(cols.index('Modified Dates')))
data = data.reindex(columns=cols)
data.drop(['Dates'], axis=1)


selected_cols = data[['Currency', "Modified Dates", 'Total Long', 'Total Short', 'Noncommercial Long', 'Noncommercial Short', 'Commercial Long', 'Commercial Short', 'Nonreportable Positions Long', 'Nonreportable Positions Short']]

df = selected_cols.copy()

total_long = df['Total Long'].tolist()
total_short = df['Total Short'].tolist()
net_total = []
for i in range(len(total_long)):
    net_total.append(total_long[i] - total_short[i])

commercial_long = df['Commercial Long'].tolist()
commercial_short = df['Commercial Short'].tolist()
net_commercial = []
for i in range(len(commercial_long)):
    net_commercial.append(commercial_long[i] - commercial_short[i])

noncommercial_long = df['Noncommercial Long'].tolist()
noncommercial_short = df['Noncommercial Short'].tolist()
net_noncommercial = []
for i in range(len(noncommercial_long)):
    net_noncommercial.append(noncommercial_long[i] - noncommercial_short[i])

df['Total'] = net_total
df['Commercial'] = net_commercial
df['Non Commercial'] = net_noncommercial


'''
Plotly Graph 
'''

df_long = pd.melt(df, id_vars=['Modified Dates'], value_vars=['Total', 'Commercial', 'Non Commercial'])

fig = px.line(df_long, x='Modified Dates', y='value', color='variable')

fig.update_layout(
    title={
        'text': "AUD (Non Commercial / Commercial / Total)",
        'y': 0.975,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Dates",
    yaxis_title="No. of Positions"
)

fig.show()
