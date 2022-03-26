from datetime import datetime
from operator import indexOf
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import HistoryRequest, LogData
from vnpy.trader.rqdata import rqdata_client
from vnpy.trader.database import database_manager
import time
import redis
from math import *
import traceback
import pandas as pd
import pyfolio as pf
import backtrader.indicator as btind
# Create a subclass of Strategy to define the indicators and logic

class MyStrategy(bt.Strategy):

    def __init__(self):

        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()

        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1

        self.buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)

    def next(self):
        if self.buy_sig:
            self.buy()
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
    # app = create_qapp()
symbol = "IF2201"

exchange = Exchange.CFFEX
start = datetime(2021, 12, 1)
end = datetime(2022, 3, 17)
interval = Interval.MINUTE
bars = database_manager.load_bar_data(
    symbol, Exchange.CFFEX, interval=Interval.MINUTE, start=start, end=end
)
if not bars or len(bars) == 0:

    req = HistoryRequest(
        symbol=symbol,
        exchange=exchange,
        interval=Interval.MINUTE,
        start=start,
        end=end,
    )

    try:
        bars = rqdata_client.query_history(req)

        if bars:
            database_manager.save_bar_data(bars)
            print(f"{symbol}-{interval}历史数据下载完成")
        else:
            print(f"数据下载失败，无法获取{symbol}的历史数据")
    except Exception:
        msg = f"数据下载失败，触发异常：\n{traceback.format_exc()}"
        print(msg)
# dataframe = pandas.read_csv(datapath,
#                             skiprows=skiprows,
#                             header=header,
#                             parse_dates=True,
#                             index_col=0)
arr =    [
        {
            "Close": s.close_price,
            "Low": s.low_price,
            "High": s.high_price,
            "Open": s.open_price,
            "Volume": s.volume,
            "Datetime":s.datetime
        }
        for s in bars
    ]
df = pd.DataFrame(
   arr
)
df.set_index(["Datetime"], inplace=True)
# if not args.noprint:
#     print('--------------------------------------------------')
#     print(df)
#     print('--------------------------------------------------')

# Pass it to the backtrader datafeed and add it to the cerebro
data = bt.feeds.PandasData(dataname=df)
# data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                #  fromdate=datetime(2011, 1, 1),
                                #  todate=datetime(2012, 12, 31))

cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

thestrats = cerebro.run()
thestrat = thestrats[0]
# pyfolio = thestrats.analyzers.getbyname('pyfolio')
pyfoliozer = thestrat.analyzers.getbyname('pyfolio')
# returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
print(pyfoliozer.get_pf_items())
# start = datetime(2021, 12, 1)
# end = datetime(2022, 3, 17)
# pf.create_full_tear_sheet(
#     returns,
#     positions=positions,
#     transactions=transactions,
#     # gross_lev=gross_lev,
#     live_start_date='2021-12-01',  # This date is sample specific
#     round_trips=True)
print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
# cerebro.plot()  # and plot it with a single command

close_over_sma = self.data.close > self.sma
bt.LinePlotterIndicator(close_over_sma, name='Close_over_SMA')