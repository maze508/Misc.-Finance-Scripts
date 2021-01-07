import pandas as pd
import os
import quandl
import time
import datetime as dt
from matplotlib import pyplot as plt


auth_tok = "``` Insert Quandl Token Here  ```"
CoT_Key = 'CFTC/232741_F_L_ALL'
this_friday = dt.date.today()
last_friday = this_friday - dt.timedelta(days=13)
last_fiveyears = this_friday - dt.timedelta(days=(365*5)+13)
# pd.set_option('display.max_columns', 500)

data = quandl.get(CoT_Key, trim_start=last_fiveyears, trim_end=this_friday, authtoken=auth_tok)
number_list = data['Noncommercial Short'].tolist()

net_noncommercial = []
net_commercial = []
net_total = []
net_nonreportable = []


for x in range(len(number_list)):


    noncommercial_long = data["Noncommercial Long"].tolist()
    noncommercial_short = data["Noncommercial Short"].tolist()
    net_noncommercial.append(noncommercial_long[x] - noncommercial_short[x])

    commercial_long = data["Commercial Long"].tolist()
    commercial_short = data["Commercial Short"].tolist()
    net_commercial.append(commercial_long[x] - commercial_short[x])

    total_long = data["Total Long"].tolist()
    total_short = data["Total Short"].tolist()
    net_total.append(total_long[x] - total_short[x])

    nonreportable_long = data["Nonreportable Positions Long"].tolist()
    nonreportable_short = data["Nonreportable Positions Short"].tolist()
    net_nonreportable.append(nonreportable_long[x] - nonreportable_short[x])

    open_interest = data["Open Interest"].tolist()


dates = data.index.tolist()


plt.style.use('seaborn')

fig1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
fig2, ax3 = plt.subplots(nrows=1, ncols=1)

ax1.plot(dates, net_commercial, label='Net Commercial Trend', linewidth=2)
ax1.plot(dates, commercial_long, label='Commercial Long Trend', linestyle='--', linewidth=1)
ax1.plot(dates, commercial_short, label='Commercial Short Trend', linestyle='--', linewidth=1)

ax2.plot(dates, net_noncommercial, label='Net Non - Commercial Trend', linewidth=2)
ax2.plot(dates, noncommercial_long, label='Non - Commercial Long Trend', linestyle='--', linewidth=1)
ax2.plot(dates, noncommercial_short, label='Non - Commercial Short Trend', linestyle='--', linewidth=1)

ax3.plot(dates, net_total, label='Net Total Trend', linewidth=2)
ax3.plot(dates, total_long, label='Total Long Trend', linestyle='--', linewidth=1)
ax3.plot(dates, total_short, label='Total Short Trend', linestyle='--', linewidth=1)

ax1.set_title('Net Commercial')
ax2.set_title('Net Non - Commercial')
ax3.set_title('Net Total')

ax1.set_xlabel("Date")
ax1.set_ylabel("Net Commercial")

ax2.set_xlabel("Date")
ax2.set_ylabel("Net Non - Commercial")

ax3.set_xlabel("Date")
ax3.set_ylabel("Net Total")

ax1.legend()
ax2.legend()
ax3.legend()

plt.tight_layout()

plt.show()





