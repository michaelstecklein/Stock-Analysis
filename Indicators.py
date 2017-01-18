from Database import *





NULL_INDICATOR_VALUE = -2



def __RSIs_list(expTF, N, closes_arr):
	rsi_arr = []
	gain_total = 0
	loss_total = 0
	for i in range(1, len(closes_arr)):
		curr_gain = 0
		curr_loss = 0
		diff = closes_arr[i] - closes_arr[i-1]
		if diff >= 0:
			curr_gain = diff
			gain_total += diff
		else:
			curr_loss = diff * -1
			loss_total += diff * -1
		if i <= N:
			rsi_arr.append(NULL_INDICATOR_VALUE)
			continue
		elif i == N+1: # first RSI value
			avg_gain = gain_total / N
			avg_loss = loss_total / N
		elif expTF:
			k = 2 / (N + 1)
			avg_gain = curr_gain * k  +  avg_gain * (1 - k)
			avg_loss = curr_loss * k  +  avg_loss * (1 - k)
		else:
			avg_gain = (avg_gain * (N-1) + curr_gain) / N
			avg_loss = (avg_loss * (N-1) + curr_loss) / N
		if avg_loss == 0:
			RSI = 100
		else:
			RS = avg_gain / avg_loss
			RSI = 100 - (100 / (1 + RS))
		rsi_arr.append(RSI)
	return rsi_arr

def RSI_list(N, closes_arr):
	# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
	return __RSIs_list(False, N, closes_arr)
	
def RSIExp_list(N, closes_arr):
	# http://www.iexplain.org/rsi-how-to-calculate-it/
	return __RSIs_list(True, N, closes_arr)

def __RSIs(expTF, N, ticker, date):
	closes_result = query("SELECT close FROM DailyData WHERE ticker='{0}' AND date<='{1}' ORDER BY date DESC LIMIT {2}".format(ticker,date,N*N))
	closes_arr = [element for tupl in closes_result for element in tupl]
	if len(closes_arr) == 0:
		log_error("No entries found for RSI of {0} on {1}".format(ticker,date))
		return
	closes_arr.reverse()
	if expTF:
		rsi_arr = RSIExp_list(N, closes_arr)
	else:
		rsi_arr = RSI_list(N, closes_arr)
	return rsi_arr[-1]

def RSI(N, ticker, date):
	return __RSIs(False, N, ticker, date)

def RSIExp(N, ticker, date):
	return __RSIs(True, N, ticker, date)










'''
def __update_RSIs(expTF):
	if expTF:
		print "updating RSIExp"
		indicator_name = "RSIExp"
		calc_method = RSIExp
		N = 22
	else:
		print "updating RSI"
		indicator_name = "RSI"
		calc_method = RSI
		N = 14
	result = query("SELECT ticker, date FROM DailyData WHERE {0}=-1 ORDER BY date ASC;".format(indicator_name))
	for row in result:
		ticker = row[0]
		date = row[1]
		closes_result = query("SELECT close FROM DailyData WHERE ticker='{0}' AND date<='{1}' ORDER BY date DESC LIMIT {2}".format(ticker,date,N+1))
		closes_arr = [element for tupl in closes_result for element in tupl]
		rsi_arr = calc_method(N, closes_arr)
		query("UPDATE DailyData SET {0}={1} WHERE ticker='{2}' AND date='{3}';".format(indicator_name,rsi_arr[-1],ticker,date))
		

def __update_RSI():
	__update_RSIs(False)

def __update_RSIExp():
	__update_RSIs(True)

def update_indicators():
	__update_RSI()
	__update_RSIExp()
'''
