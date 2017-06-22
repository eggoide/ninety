#!/usr/bin/python
#Ondrej Musil 2017-06-08

import sys
import os
import pandas as pd
import pandas_datareader.data as web
import datetime
from stockstats import StockDataFrame as Sdf
import warnings
from pandas.tseries.offsets import BDay

config_file = open("/home/vboxuser/ninety/config/sp100.csv", "r").readlines()
output_dir = '/home/vboxuser/ninety/output/'
initial_capital = 10000
initial_capital_shares = 10
RSI_threshold = 10
max_number_of_positions = 2
max_number_of_iterations = 4
TWS_IP = '127.0.0.1'
TWS_PORT = '4096'
TWS_ID = '101'

warnings.filterwarnings('ignore')

def removeFile(removeFileName):
    try:
        os.remove(removeFileName)
    except OSError:
        pass
  
def firstBuy(tick1):
    if os.path.isfile("%s%s.csv" % (output_dir, tick1)) is True:
        reBuy(tick1)
    else:
        firstBuyFile = open("%s%s.csv" % (output_dir, tick1), "w") 
        firstBuyCapital = initial_capital / 10
        firstBuySharesCount = firstBuyCapital / minRSIlastDayClose
        firstBuySharesValue = minRSIlastDayClose * round(firstBuySharesCount, 0)
        print "Buying ticker %s , %s shares for %s" % (tick1, round(firstBuySharesCount, 0), firstBuySharesValue)
        print >>firstBuyFile, "%s;%s;%s;%s;%s;%s" % (tick1, today, last_close_date, minRSIlastDayClose, lastDayRsi, firstBuyCapital)
        firstBuyFile.close()
    
def reBuy(tick1):
    #secondBuyCapital = (initial_capital / 10) * 2
    print "REBUY %s" % tick1

def sell(tick1):
    pass
    removeFile("%s%s.csv" % (output_dir, tick1))
    
#removeFileName('/home/vboxuser/test/data/tmp/out.csv')

filteredList = []

for ticker in config_file:
    now = datetime.date.today()
    from_date = now - datetime.timedelta(days=201)
    last_close_date = now - BDay(1)
    day_before_last_close_date = now - BDay(2)
    today = now
    #data = web.DataReader(ticker, 'google', from_date, last_close_date)
    data = web.DataReader(ticker, 'google', '2016-04-01', last_close_date)
    
    stock_df = Sdf.retype(data)
    data['rsi']=stock_df['rsi_2']
    data['sma200']=stock_df['close_200_sma']
    data['sma5']=stock_df['close_5_sma']
    
    del data['high']
    del data['low']
    del data['open']
    del data['volume']
    #del data['close_-1_s']
    #del data['close_-1_d']
    del data['rs_2']
    del data['rsi_2']
    del data['close_200_sma']
    del data['close_5_sma']

    #print "TICKER NAME:", ticker.rstrip()
    #print "LAST DAY:", last_close_date.date()
    #print "DAY BEFORE LAST DAY:", day_before_last_close_date.date()
    lastDayClose = round(data.loc[last_close_date]['close'], 2)
    #print "LAST DAY CLOSE:", lastDayClose
    dayBeforeLastDayClose = data.loc[day_before_last_close_date]['close']
    #print "DAY BEFORE LAST DAY CLOSE:", dayBeforeLastDayClose
    lastDayRsi = round(data.loc[last_close_date]['rsi'], 3)
    #print "LAST DAY RSI:", lastDayRsi
    lastDaySma200 = round(data.loc[last_close_date]['sma200'], 2)
    #print "LAST DAY SMA200:", lastDaySma200
    lastDaySma5 = round(data.loc[last_close_date]['sma5'], 2)
    #print "LAST DAY SMA5:", lastDaySma5
    #print " "

    # if lastDayClose > dayBeforeLastDayClose:
        # print "Cena STOUPA"
    # elif lastDayClose < dayBeforeLastDayClose:
        # print "Cena KLESA"
    # elif lastDayClose == dayBeforeLastDayClose:
        # print "Cena STEJNA"
    if lastDayRsi < RSI_threshold and lastDayClose > lastDaySma200:
        print "Ticker match: %s , RSI: %s" % (ticker.rstrip(), lastDayRsi)
        #print >>filteredTickersFile, "%s;%s;%s;%s;%s" % (last_close_date,lastDayClose,ticker.rstrip(), lastDayRsi, initial_capital)
        filteredList.append ({'key1':last_close_date, 'key2':lastDayClose, 'key3':ticker.rstrip(), 'key4':lastDayRsi})
        
        
    # if lastDayRsi < 100 :
        # print "Cena pod RSI(2) 10"
    # if lastDayClose > lastDaySma200:
        # print "Cena nad SMA200"
    # if lastDayClose > lastDaySma5:
        # print "Cena nad SMA5"
    #print " "

# filteredTickersFile.close()        

#filteredListRaw = open("/home/vboxuser/test/data/tmp/out.csv", "r")

#print "filtered:" , filtered.read()
#filteredList = filteredListRaw.readlines()
#filteredList = [x.strip() for x in filteredList]
#filteredListRaw.close()

#print "filtered list: %s" % filteredList
filesCounter = next(os.walk('%s' % output_dir))[2]
filesNumber = len(filesCounter) 

if not filteredList:
    print "No ticker meets criteria of RSI(2) below 10" % RSI_threshold
else:
    if filesNumber < max_number_of_positions:
        print ""
        minRSIticker = min(filteredList, key=lambda x:x['key4'])['key3']
        minRSI = min(filteredList, key=lambda x:x['key4'])['key4']
        minRSIlastDayClose = min(filteredList, key=lambda x:x['key4'])['key2']
        print "Winning ticker: %s, RSI: %s, PRICE: %s " % (minRSIticker, minRSI, minRSIlastDayClose)
        #FIRST BUY
        firstBuy(minRSIticker)
    else:
        print "All available positions are already opened"

# for filteredTicker in filteredList:
    # tickers = filteredTicker.split(';')
    # print(tickers[2]), (tickers[3])
    

        
