from Database import *





DEFAULT_TABLE_VALUE = -1
NULL_INDICATOR_VALUE = -2



'''
def RSI_list(N, closes_arr):
	# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
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

def RSI(N, ticker, date):
	closes_result = query("SELECT close FROM DailyData WHERE ticker='{0}' AND date<='{1}' ORDER BY date DESC LIMIT {2}".format(ticker,date,N*N))
	closes_arr = [element for tupl in closes_result for element in tupl]
	if len(closes_arr) == 0:
		log_error("No entries found for RSI of {0} on {1}".format(ticker,date))
		return
	closes_arr.reverse()
	rsi_arr = RSI_list(N, closes_arr)
	return rsi_arr[-1]
'''


'''
__RSI_COL_NAME = "RSI14"
__N = 14
def __create_RSI_col():
	result = query("DESCRIBE {}".format(DAILYDATA_TABLE_NAME))
	for row in result:
		if row[0] == __RSI_COL_NAME:
			return
	query("ALTER TABLE {0} ADD {1} FLOAT NULL DEFAULT {2}".format(DAILYDATA_TABLE_NAME,__RSI_COL_NAME,DEFAULT_TABLE_VALUE))

def __update_rsi(ticker, date, rsi_val):
	query("UPDATE DailyData SET {}={} WHERE ticker='{}' AND date='{}';".format(__RSI_COL_NAME,rsi_val,ticker,date))

def __update_ticker_RSI(ticker):
	result = query("SELECT date, close, {} FROM DailyData WHERE ticker='{}' ORDER BY date ASC;".format(__RSI_COL_NAME,ticker))
	rsi_list = []
	cummulative_gain = 0
	cummulative_loss = 0
	for i in range(0, len(result)):
		row = result[i]
		date = row[0]
		close = row[1]
		curr_rsi = row[2]
		# gain and loss
		gain = 0
		loss = 0
		if i > 0:
			prev_close = result[i-1][1]
			diff = close - prev_close
			if diff > 0:
				gain = diff
			else:
				loss = diff * -1
		# calculate rsi
		if i < __N:
			cummulative_gain += gain
			cummulative_loss += loss
			__update_rsi(ticker, date, NULL_INDICATOR_VALUE)
			continue
		elif i == __N:
			avg_gain = cummulative_gain
			avg_loss = cummulative_loss
		else:
			avg_gain = (avg_gain * (__N-1) + gain) / __N
			avg_loss = (avg_loss * (__N-1) + loss) / __N
		if avg_loss == 0:
			RSI = 100
		else:
			RS = avg_gain / avg_loss
			RSI = 100 - (100 / (1 + RS))
		__update_rsi(ticker, date, RSI)

def __update_RSI():
	tickers = get_Stocks_tickers()
	tickers.extend(get_Indices_tickers())
	for ticker in tickers:
		log("Updating ticker RSI: {}".format(ticker))
		__update_ticker_RSI(ticker)
'''

'''
def __avg_gain(prices_list):
	pass # TODO

def __calc_rsi(ticker, date):
	result = query("SELECT date, rsi FROM DailyData WHERE ticker='{}' AND date<='{}' ORDER BY date DESC LIMIT {}".format(ticker,date,__N+2))
	# not enough data points yet
	if len(result) <= __N:
		return NULL_INDICATOR_VALUE
	# first rsi point
	if len(result) == __N+1:
		prices_list = []
		for row in result:
			prices_list.append(row[1])
		avg_gain = __avg_gain(prices_list)
		avg_loss = __avg_loss(prices_list)
		rs = avg_gain / avg_loss
		rsi = 100 - (100 / (1 + rs))
		return rsi
	# rsi is calculated from previous rsi
	prev_rsi = result[1][1] # previous date's rsi
	if prev_rsi == DEFAULT_TABLE_VALUE:
		prev_rsi = __calc_rsi(ticker, result[1][0]) # calc previous date's rsi
	rsi = (13 * prev_rsi + # TODO left off here

def __update_RSI():
	__create_RSI_col()
	print "updating RSI"
	result = query("SELECT ticker, date FROM DailyData WHERE {0}=-1 ORDER BY date ASC;".format(__RSI_COL_NAME))
	for row in result:
		ticker = row[0]
		date = row[1]
		rsi = __calc_rsi(ticker, date)
		query("UPDATE DailyData SET {0}={1} WHERE ticker='{2}' AND date='{3}';".format(__RSI_COL_NAME,rsi,ticker,date))
'''

__RSI_TABLE_NAME = "RSIs"

def __create_table():
	# make table
	QUERY = """	CREATE TABLE IF NOT EXISTS {}(
			ticker VARCHAR(5) NOT NULL,
			date DATE NOT NULL,
			RSI FLOAT NULL DEFAULT {},
			avg_gain FLOAT NULL DEFAULT{},
			avg_loss FLOAT NULL DEFAULT{},
			PRIMARY KEY(ticker, date)); """.format(__RSI_TABLE_NAME,DEFAULT_TABLE_VALUE,DEFAULT_TABLE_VALUE,DEFAULT_TABLE_VALUE)
	query(QUERY)
	# add stock and indice tickers and dates
	results = query("SELECT ticker, date FROM DailyData;")
	for row in results:
		ticker = row[0]
		date = row[1]
		insert(__RSI_TABLE_NAME, "'{}','{}',NULL,NULL,NULL".format(ticker,date))
	

def __update_RSI():
	__create_table()

def update_indicators():
	log("Updating RSIs")
	__update_RSI()
