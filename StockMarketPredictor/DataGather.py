# %%
import yfinance as yf
from datetime import datetime
from NumericalMethods import *

#ticker = "^GSPC"
ticker = "BTC-USD"
stock_ticker = yf.Ticker(ticker)
interval = "1"

start_day = datetime(2022, 5, 1, 0, 0, 0, 0)
end_day = datetime(2022, 5, 7, 0, 0, 0, 0)
#day_info = stock_ticker.history(period='1d')
#day_info = stock_ticker.history(start = "2022-03-18", end = "2022-03-18", interval="{0}m".format(interval))
#day_info = stock_ticker.history(start = "2022-05-04", end = "2022-05-05", interval="{0}m".format(interval))
#day_info = stock_ticker.history(start = "2022-05-05", end = "2022-05-06", interval="{0}m".format(interval))
#day_info = stock_ticker.history(start = "2022-05-06", end = "2022-05-07", interval="{0}m".format(interval))

day_info = stock_ticker.history(start = start_day, end = end_day, interval="{0}h".format(interval))
value_count = 0

with open("yFile.txt", "w") as data_file:
    with open("xFile.txt", "w") as x_file:
    #file.write(interval+"\n")
        for index, row in day_info.iterrows():
            
            if index.hour % 2 == 0:
                print(index)
                data_file.write(str(round(row["Open"], 2))+"\n")
                x_file.write(str((2*60)*value_count)+"\n")
                value_count += 1

                if value_count == len(day_info) - 1:
                    data_file.write(str(round(row["Close"], 2))+"\n")
                    x_file.write(str(int(interval)*value_count)+"\n")
                    break

# %%
