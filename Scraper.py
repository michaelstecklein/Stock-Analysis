import requests
import csv
import datetime
from bs4 import BeautifulSoup
from Database import *
from Log import *



SP500 = "S&P500"
DJI = "DJI"
NASDAQ = "NASDAQ"

SHOULD_SCRAPE_NYSE = False






class DailyPrices:
	date = datetime.date.today()
	openn = 0.0
	high = 0.0
	low = 0.0
	close = 0.0
	volume = 0
	adj_close = 0.0
	def __init__(self,d,o,h,l,c,v,a):
		self.date = d
		self.openn = o
		self.high = h
		self.low = l
		self.close = c
		self.volume = v
		self.adj_close = a


def __get_price_history(ticker, start_date=datetime.date(1962,1,2), end_date=datetime.date.today()):
	log("Getting price history for {0}".format(ticker))
	page = requests.get('http://chart.finance.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv'.format(ticker,start_date.month-1,start_date.day,start_date.year,end_date.month-1,end_date.day,end_date.year))
	prices = csv.reader(page.text.splitlines())
	daily_price_list = []
	for p in prices:
		days_price = DailyPrices(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
		daily_price_list.append(days_price)
	return daily_price_list[1:]


def scrape_price_history(ticker, start_date=None):
	# scrape price history
	if start_date is None:
		prices = __get_price_history(ticker)
	else:
		prices = __get_price_history(ticker,start_date=start_date)
	# populate db
	for p in prices:
		insert_DailyData_table(ticker,p.date,p.openn,p.high,p.low,p.close,p.volume,p.adj_close)
	# set first_data_date for stock
	if start_date is None:
		first_data_date = prices[-1].date
		update_Stocks_first_data_date(ticker,first_data_date)
		update_Indices_first_data_date(ticker,first_data_date)

def update_stock_prices():
	'''
	sp500_stocks = get_Stocks_for_indice(SP500)
	dji_stocks = get_Stocks_for_indice(DJI)
	tickers = list( set(sp500_stocks) | set(dji_stocks) )
	if SHOULD_SCRAPE_NYSE:
		all_tickers = get_Stocks_for_indice(None)
		tickers = all_tickers
	'''
	tickers = get_Stocks_tickers() # all tickers
	for ticker in tickers:
		last_update = get_Stocks_last_update(ticker)
		if last_update is None:
			scrape_price_history(ticker)
		else:
			scrape_price_history(ticker,start_date=last_update)
		update_Stocks_last_update(ticker)





__reference_stocks = ('IBM','KO','GE')
def scrape_stock_dates(start_date=None):
	if start_date is None:
		clear_MarketDates_table()
	else:
		reset_MarketDates_table()
	daily_price_lists = []
	for ticker in __reference_stocks:
		if start_date is None:
			daily_price_lists.append(__get_price_history(ticker))
		else:
			daily_price_lists.append(__get_price_history(ticker,start_date=start_date)[:-1])
	for i in reversed(range(1, len(daily_price_lists[0]))):
		date = daily_price_lists[0][i].date
		for l in daily_price_lists:
			if date != l[i].date:
				log_error("Dates do not match in 'scrape_stock_dates': {0}  {1}".format(date,l[i].date), shutdown=True)
		insert_MarketDates_table(date)


def update_stock_dates():
	last_update = get_last_update_MarketDates()
	if last_update == datetime.date.today():
		return
	scrape_stock_dates(start_date=last_update)





def scrape_SP500():
	page = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = BeautifulSoup(page.text,"lxml")
	table = soup.find_all('table')[0]
	sp500_tickers = []

	# parse and insert into db
	for row in table.find_all('tr')[1:]:
		cols = row.find_all('td')
		ticker = cols[0].a.text
		company_name = cols[1].a.text
		sp500_tickers.append(ticker)
		insert_Stocks_table(ticker,company_name)

	# update S&P500 entries in the db
	for row in query("SELECT ticker, indices FROM {0}".format(STOCKS_TABLE_NAME)):
		ticker = row[0]
		indices = row[1]
		isInSP500 = sp500_tickers.count(ticker) > 0
		if SP500 not in indices and isInSP500:
			if indices == '':
				update_Stocks_indices(SP500,ticker)
			else:
				update_Stocks_indices("{0},{1}".format(indices,SP500),ticker)
		if SP500 in indices and not isInSP500:
			withComma = "{},".format(SP500)
			if withComma in indices:
				update_Stocks_indices(indices.replace(withComma,''),ticker)
			else:
				update_Stocks_indices(indices.replace(SP500,''),ticker)
	



def scrape_DJI():
	page = requests.get('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
	soup = BeautifulSoup(page.text,"lxml")
	table = soup.find_all('table')[1]
	dji_tickers = []

	# parse and insert into db
	for row in table.find_all('tr')[1:]:
		cols = row.find_all('td')
		ticker = cols[2].a.text
		company_name = cols[0].a.text
		dji_tickers.append(ticker)
		insert_Stocks_table(ticker,company_name)

	# update DJI entries in the db
	for row in query("SELECT ticker, indices FROM {0}".format(STOCKS_TABLE_NAME)):
		ticker = row[0]
		indices = row[1]
		isInDJI = dji_tickers.count(ticker) > 0
		if DJI not in indices and isInDJI:
			if indices == '':
				update_Stocks_indices(DJI,ticker)
			else:
				update_Stocks_indices("{0},{1}".format(indices,DJI),ticker)
		if DJI in indices and not isInDJI:
			withComma = "{},".format(DJI)
			if withComma in indices:
				update_Stocks_indices(indices.replace(withComma,''),ticker)
			else:
				update_Stocks_indices(indices.replace(DJI,''),ticker)


def scrape_NASDAQ():
	pass


def scrape_NYSE():
	page = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download')
	reader = csv.reader(page.text.splitlines())
	for entry in reader:
		ticker = entry[0]
		company_name = entry[1]
		insert_Stocks_table(ticker,company_name)
	
def scrape_indices():
	scrape_SP500()
	scrape_DJI()
	scrape_NASDAQ()
	if SHOULD_SCRAPE_NYSE:
		scrape_NYSE()
