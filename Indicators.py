from Database import *





DEFAULT_INDICATOR_VALUE = -1
NULL_INDICATOR_VALUE = -2



############################################################################################################
#						RSI
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
############################################################################################################
__N = 14
__RSI_TABLE_NAME = "RSIs"

def RSI(ticker, date):
	result = query("SELECT RSI, date FROM {} WHERE ticker='{}' AND date<='{}' ORDER BY date DESC LIMIT 1;".format(__RSI_TABLE_NAME, ticker, date))
	print ticker, "  ", date, "  ", result
	if len(result) == 0:
		log_error("No RSI data found for {} {}".format(ticker,date))
		return NULL_INDICATOR_VALUE
	return result[0][0]

def __create_rsi_table():
	log("Creating/updating RSI table")
	# make table
	QUERY = """	CREATE TABLE IF NOT EXISTS {}(
			ticker VARCHAR(5) NOT NULL,
			date DATE NOT NULL,
			RSI FLOAT NULL DEFAULT {},
			avg_gain FLOAT NULL DEFAULT{},
			avg_loss FLOAT NULL DEFAULT{},
			PRIMARY KEY(ticker, date)); """.format(__RSI_TABLE_NAME,DEFAULT_INDICATOR_VALUE,DEFAULT_INDICATOR_VALUE,DEFAULT_INDICATOR_VALUE)
	query(QUERY)
	# add stock and indice tickers and dates
	query("INSERT IGNORE INTO {} (ticker, date, RSI, avg_gain, avg_loss) SELECT ticker, date, {}, {}, {} FROM DailyData;".format(__RSI_TABLE_NAME,DEFAULT_INDICATOR_VALUE,DEFAULT_INDICATOR_VALUE,DEFAULT_INDICATOR_VALUE))

def __get_prev_rsi(ticker, date):
	result = query("SELECT RSI,avg_gain,avg_loss FROM {} WHERE ticker='{}' AND date<'{}' ORDER BY date DESC LIMIT 1;".format(__RSI_TABLE_NAME,ticker,date))
	if len(result) == 0:
		return None
	return result[0]

def __get_close_history(ticker, date, n_days):
	result = query("SELECT close FROM DailyData WHERE ticker='{}' AND date<='{}' ORDER BY date DESC LIMIT {};".format(ticker,date,n_days))
	return [element for tupl in result for element in tupl]

def __update_ticker_RSI(ticker):
	result = query("SELECT date FROM {} WHERE ticker='{}' AND RSI={} ORDER BY date ASC;".format(__RSI_TABLE_NAME,ticker,DEFAULT_INDICATOR_VALUE))
	dates = [element for tupl in result for element in tupl]
	if len(dates) == 0:
		return
	prev = __get_prev_rsi(ticker, dates[0])
	for date in dates:
		# Get previous values
		if prev != None:
			prev_rsi = prev[0]
			prev_avg_gain = prev[1]
			prev_avg_loss = prev[2]
		# Calculate rsi
		avg_gain = NULL_INDICATOR_VALUE
		avg_loss = NULL_INDICATOR_VALUE
		if prev == None: # first entry
			rsi = NULL_INDICATOR_VALUE
			avg_gain = NULL_INDICATOR_VALUE
			avg_loss = NULL_INDICATOR_VALUE
		elif prev_rsi == DEFAULT_INDICATOR_VALUE:
			raise RuntimeError("Previous RSI entry should have a default value due to query ordering")
		elif prev_rsi == NULL_INDICATOR_VALUE:
			count = query("SELECT COUNT(*) FROM {} WHERE ticker='{}' AND date<='{}';".format(__RSI_TABLE_NAME,ticker,date))[0][0]
			if count < __N:
				rsi = NULL_INDICATOR_VALUE
				avg_gain = NULL_INDICATOR_VALUE
				avg_loss = NULL_INDICATOR_VALUE
			elif count > __N:
				raise RuntimeError("More than first N entries have a NULL value for RSI of ticker {}".format(ticker))
			else: # first rsi value
				closes = __get_close_history(ticker, date, __N+1)
				closes.reverse()
				avg_gain = 0
				avg_loss = 0
				for i in range(1, len(closes)):
					diff = closes[i] - closes[i-1]
					if diff > 0:
						avg_gain = diff
						avg_loss = 0
					else:
						avg_gain = 0
						avg_loss = diff * -1
				if avg_loss != 0:
					rs = avg_gain / avg_loss
					rsi = 100 - 100 / (1 + rs)
				else:
					rsi = 100
		else: # rsi values other than the first
			closes = __get_close_history(ticker, date, 2)
			diff = closes[0] - closes[1]
			if diff > 0:
				curr_gain = diff
				curr_loss = 0
			else:
				curr_gain = 0
				curr_loss = diff * -1
			avg_gain = (prev_avg_gain * (__N-1) + curr_gain) / __N
			avg_loss = (prev_avg_loss * (__N-1) + curr_loss) / __N
			if avg_loss != 0:
				rs = avg_gain / avg_loss
				rsi = 100 - 100 / (1 + rs)
			else:
				rsi = 100
		# Update with calculated rsi, avg_gain, and avg_loss values
		query("UPDATE {} SET RSI={}, avg_gain={}, avg_loss={} WHERE ticker='{}' AND date='{}';".format(__RSI_TABLE_NAME,rsi,avg_gain,avg_loss,ticker,date))
		prev = (rsi, avg_gain, avg_loss)

def __update_RSI():
	#__create_rsi_table()
	result = query("SELECT DISTINCT(ticker) FROM {} WHERE RSI={};".format(__RSI_TABLE_NAME,DEFAULT_INDICATOR_VALUE))
	for row in result:
		ticker = row[0]
		log("Updating RSI for '{}'".format(ticker))
		__update_ticker_RSI(ticker)

def update_indicators():
	log("Updating RSIs")
	__update_RSI()
