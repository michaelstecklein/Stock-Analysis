import datetime
from Indicators import *




update_indicators()



'''
ticker = 'FB'
date = datetime.date.today()
N = 14
#closes_result = query("SELECT close FROM DailyData WHERE ticker='{0}' AND date<='{1}' ORDER BY date DESC LIMIT {2}".format(ticker,date,N*N))
closes_result = query("SELECT close FROM DailyData WHERE ticker='{0}' AND date<='{1}' AND date >= '2016-01-19' ORDER BY date DESC".format(ticker,date))
closes_arr = [element for tupl in closes_result for element in tupl]
closes_arr.reverse()
print "closes: ",closes_arr
rsilist = RSI_list(N,closes_arr)
print "RSI_list: ",rsilist
rsi = RSI(N,ticker,date)
print "RSI: ",rsi

'''





'''
rsis = RSIStrategy()
print "RESULTS:::"
print rsis.results()
'''
