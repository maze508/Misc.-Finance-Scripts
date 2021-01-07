import pandas as pd
import os
import quandl
import time
import datetime as dt
from matplotlib import pyplot as plt


auth_tok = "``` Insert Quandl Token Here  ```"
CoT_Key = 'CFTC/232741_F_L_CHG'
this_friday = dt.date.today()
last_friday = this_friday - dt.timedelta(days=13)
last_threeyears = this_friday - dt.timedelta(days=(365*3)+13)
last_fiveyears = this_friday - dt.timedelta(days=(365*5)+13)
# pd.set_option('display.max_columns', 500)

data = quandl.get(CoT_Key, trim_start=last_threeyears, trim_end=this_friday, authtoken=auth_tok)
number_list = data['Noncommercial Shorts - Change'].tolist()

net_noncommercial_change = []
net_commercial_change = []
net_total_change = []
net_nonreportable_change = []


for x in range(len(number_list)):

    noncommercial_long = data["Noncommercial Longs - Change"].tolist()
    noncommercial_short = data["Noncommercial Shorts - Change"].tolist()
    net_noncommercial_change.append(noncommercial_long[x] - noncommercial_short[x])

    commercial_long = data["Commercial Longs - Change"].tolist()
    commercial_short = data["Commercial Shorts - Change"].tolist()
    net_commercial_change.append(commercial_long[x] - commercial_short[x])

    total_long = data["Total Reportable Longs - Change"].tolist()
    total_short = data["Total Reportable Shorts - Change"].tolist()
    net_total_change.append(total_long[x] - total_short[x])

    nonreportable_long = data["Non Reportable Longs - Change"].tolist()
    nonreportable_short = data["Non Reportable Shorts- Change"].tolist()
    net_nonreportable_change.append(nonreportable_long[x] - nonreportable_short[x])

    open_interest = data["Open Interest - Change"].tolist()


dates = data.index.tolist()


plt.style.use('seaborn')

fig1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
fig2, ax3 = plt.subplots(nrows=1, ncols=1)

ax1.plot(dates, net_commercial_change, label='Net Commercial Trend Change', linewidth=2)
ax1.plot(dates, commercial_long, label='Commercial Long Trend Change', linestyle='-', linewidth=1)
ax1.plot(dates, commercial_short, label='Commercial Short Trend Change', linestyle='--', linewidth=1)

ax2.plot(dates, net_noncommercial_change, label='Net Non - Commercial Trend Change', linewidth=2)
ax2.plot(dates, noncommercial_long, label='Non - Commercial Long Trend Change', linestyle='-', linewidth=1)
ax2.plot(dates, noncommercial_short, label='Non - Commercial Short Trend Change', linestyle='--', linewidth=1)

ax3.plot(dates, net_total_change, label='Net Total Trend Change', linewidth=2)
ax3.plot(dates, total_long, label='Total Long Trend Change', linestyle='-', linewidth=1)
ax3.plot(dates, total_short, label='Total Short Trend Change', linestyle='--', linewidth=1)

ax1.set_title('Net Commercial Change')
ax2.set_title('Net Non - Commercial Change')
ax3.set_title('Net Total Change')

ax1.set_xlabel("Date")
ax1.set_ylabel("Net Commercial Change")

ax2.set_xlabel("Date")
ax2.set_ylabel("Net Non - Commercial Change")

ax3.set_xlabel("Date")
ax3.set_ylabel("Net Total Change")

ax1.legend()
ax2.legend()
ax3.legend()

plt.tight_layout()

plt.show()





