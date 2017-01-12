from Database import *





NULL_INDICATOR_VALUE = -2


def RSI_list(N, closes_arr):
	# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
	rsi_arr = []
	avg_gain = 0
	avg_loss = 0
	for i in range(0, len(closes_arr)):
		curr_gain = 0
		curr_loss = 0
		diff = 0
		if i > 0:
			diff = closes_arr[i] - closes_arr[i-1]
		if diff >= 0:
			curr_gain = diff
		else:
			curr_loss = -1 * diff
		avg_gain = (avg_gain*(N-1) + curr_gain) / N
		avg_loss = (avg_loss*(N-1) + curr_loss) / N
		if i < N:
			rsi_arr.append(NULL_INDICATOR_VALUE)
			continue
		if avg_loss == 0:
			RSI = 100
		else:
			RS = avg_gain / avg_loss
			RSI = 100 - (100 / (1 + RS))
		rsi_arr.append(RSI)
	return rsi_arr
	
def RSIExp_list(N, closes_arr):
	# http://www.iexplain.org/rsi-how-to-calculate-it/
	pass # TODO

def RSI(N, date):
	pass # TODO

def RSIExp(N, date):
	pass # TODO






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
	
