from Database import *





DEFAULT_TABLE_VALUE = -1
NULL_INDICATOR_VALUE = -2

# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi



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
	query("INSERT IGNORE INTO {} (ticker, date, RSI, avg_gain, avg_loss) SELECT ticker, date, {}, {}, {} FROM DailyData;".format(__RSI_TABLE_NAME,DEFAULT_TABLE_VALUE,DEFAULT_TABLE_VALUE,DEFAULT_TABLE_VALUE))

def __update_RSI():
	#__create_table()

def update_indicators():
	log("Updating RSIs")
	__update_RSI()
